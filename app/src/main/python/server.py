#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CADRE + SIGNATURE - Appli Android autonome (Chaquopy + Flask + WebView)
JM.DARGERE  -  @jean_michel_dargere

Meme moteur que la version PC / Termux : cadre mesure au pixel pres, vraie
signature vectorisee, placement automatique par mesure de luminosite.
Nouveautes de l'appli : apercu en direct, couleurs libres, texte + polices,
6 positions, transparence, ombre, styles de cadre, styles prets a l'emploi.
"""

import os
import io
import json
import glob
import tempfile
import threading
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from flask import Flask, request, jsonify, Response
from werkzeug.serving import make_server

IMG_EXTENSIONS = (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp")

REF_SHORT_SIDE = 1245.0
BORDER_OUTER = 32 / REF_SHORT_SIDE
BORDER_LINE = 4 / REF_SHORT_SIDE
BORDER_INNER = 12 / REF_SHORT_SIDE
CONTRAST_GOOD_ENOUGH = 100

# --- signatures VECTORISEES (contours lisses) : nettes a toute taille ---
from sig_data import FULL as _FULL, INITIALS as _INITIALS



def load_signature(style="full"):
    """Decode la signature (coordonnees en dix-milliemes, codees par differences)."""
    d = json.loads(_INITIALS if style == "initials" else _FULL)
    shapes = []
    for s in d["s"]:
        hole, flat = bool(s[0]), s[1:]
        x, y, path = flat[0], flat[1], []
        path.append([x / 10000.0, y / 10000.0])
        for i in range(2, len(flat), 2):
            x += flat[i]
            y += flat[i + 1]
            path.append([x / 10000.0, y / 10000.0])
        shapes.append({"path": path, "hole": hole})
    return {"aspect": d["a"], "shapes": shapes}


# ---------------------------------------------------------------- polices
FONT_DIRS = ["/system/fonts", "/system/font", "/usr/share/fonts"]
PREFERRED = ["DancingScript", "GreatVibes", "Pacifico", "ComingSoon", "Cursive", "NotoSerif",
             "Roboto", "Poppins", "CutiveMono", "CarroisGothicSC", "SourceSansPro", "DroidSerif",
             "Lora", "Playfair", "Montserrat", "OpenSans", "DejaVuSerif", "DejaVuSans", "LiberationSerif"]
_FONT_CACHE = None


def list_fonts():
    """Retourne {nom_affiche: chemin} des polices disponibles (regular uniquement)."""
    global _FONT_CACHE
    if _FONT_CACHE is not None:
        return _FONT_CACHE
    found = {}
    for d in FONT_DIRS:
        for p in glob.glob(os.path.join(d, "**", "*.[to]tf"), recursive=True):
            stem = os.path.splitext(os.path.basename(p))[0]
            low = stem.lower()
            if any(w in low for w in ("bold", "italic", "oblique", "light", "thin", "black", "medium",
                                      "semibold", "condensed", "extra", "mono", "symbol", "emoji")):
                continue
            if not any(stem.startswith(k) or k.lower() in low for k in PREFERRED):
                continue
            name = stem.replace("-Regular", "").replace("_", " ")
            found.setdefault(name, p)
    ordered = {}
    for k in PREFERRED:
        for n in sorted(found):
            if k.lower() in n.lower().replace(" ", "") and n not in ordered:
                ordered[n] = found[n]
    _FONT_CACHE = ordered
    return ordered


def get_font(name, size):
    fonts = list_fonts()
    path = fonts.get(name) or (next(iter(fonts.values())) if fonts else None)
    try:
        if path:
            return ImageFont.truetype(path, size)
    except Exception:
        pass
    try:
        return ImageFont.load_default(size)
    except Exception:
        return ImageFont.load_default()


# ---------------------------------------------------------------- signature
def render_vector_mask(sig_data, width_px, supersample=4):
    """Masque alpha (L) de la signature vectorielle, trous des lettres respectes."""
    aspect = sig_data["aspect"]
    width_px = max(1, int(width_px))
    height_px = max(1, round(width_px / aspect))
    W, H = width_px * supersample, height_px * supersample
    alpha = Image.new("L", (W, H), 0)
    draw = ImageDraw.Draw(alpha)
    for shape in sig_data["shapes"]:
        if not shape["hole"]:
            pts = [(x * W, y * H) for x, y in shape["path"]]
            if len(pts) >= 3:
                draw.polygon(pts, fill=255)
    for shape in sig_data["shapes"]:
        if shape["hole"]:
            pts = [(x * W, y * H) for x, y in shape["path"]]
            if len(pts) >= 3:
                draw.polygon(pts, fill=0)
    return alpha.resize((width_px, height_px), Image.LANCZOS)


def render_text_mask(text, font_name, width_px):
    """Masque alpha (L) d'un texte libre, ajuste a la largeur demandee."""
    text = (text or "").strip() or "JM.Dargere"
    big = 400
    font = get_font(font_name, big)
    probe = Image.new("L", (10, 10), 0)
    l, t, r, b = ImageDraw.Draw(probe).textbbox((0, 0), text, font=font)
    w, h = max(1, r - l), max(1, b - t)
    pad = 20
    canvas = Image.new("L", (w + 2 * pad, h + 2 * pad), 0)
    ImageDraw.Draw(canvas).text((pad - l, pad - t), text, font=font, fill=255)
    bbox = canvas.getbbox()
    if bbox:
        canvas = canvas.crop(bbox)
    width_px = max(1, int(width_px))
    height_px = max(1, round(canvas.height * width_px / canvas.width))
    return canvas.resize((width_px, height_px), Image.LANCZOS)


def build_mask(P, width_px):
    kind = P.get("sig_kind", "initials")
    if kind == "text":
        return render_text_mask(P.get("sig_text", ""), P.get("sig_font", ""), width_px)
    return render_vector_mask(load_signature("full" if kind == "full" else "initials"), width_px)


def mask_aspect(P):
    kind = P.get("sig_kind", "initials")
    if kind == "text":
        m = render_text_mask(P.get("sig_text", ""), P.get("sig_font", ""), 400)
        return m.width / m.height
    return load_signature("full" if kind == "full" else "initials")["aspect"]


# ---------------------------------------------------------------- cadre
def hex_rgb(h, default=(0, 0, 0)):
    try:
        h = h.lstrip("#")
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    except Exception:
        return default


STYLES = {
    "classic": ((0, 0, 0), (255, 255, 255), (0, 0, 0)),
    "white": ((255, 255, 255), (0, 0, 0), (255, 255, 255)),
}


def add_frame(img_rgb, P):
    w, h = img_rgb.size
    short_side = min(w, h)
    k = max(0.2, float(P.get("frame_thick", 100)) / 100.0)
    b_out = max(1, round(short_side * BORDER_OUTER * k))
    b_line = max(1, round(short_side * BORDER_LINE * k))
    b_in = max(1, round(short_side * BORDER_INNER * k))
    total = b_out + b_line + b_in
    style = P.get("frame_style", "classic")
    if style in STYLES:
        c_out, c_line, c_in = STYLES[style]
    else:
        c_out = hex_rgb(P.get("frame_outer", "#000000"))
        c_line = hex_rgb(P.get("frame_line", "#ffffff"), (255, 255, 255))
        c_in = hex_rgb(P.get("frame_inner", "#000000"))
    new_w, new_h = w + 2 * total, h + 2 * total
    canvas = Image.new("RGB", (new_w, new_h), c_out)
    d = ImageDraw.Draw(canvas)
    x0, y0, x1, y1 = b_out, b_out, new_w - b_out, new_h - b_out
    d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=c_line)
    d.rectangle([x0 + b_line, y0 + b_line, x1 - b_line - 1, y1 - b_line - 1], fill=c_in)
    canvas.paste(img_rgb, (total, total))
    return canvas, total


# ---------------------------------------------------------------- placement
def region_luminance(img, box):
    box = (max(0, box[0]), max(0, box[1]), min(img.width, box[2]), min(img.height, box[3]))
    if box[2] <= box[0] or box[3] <= box[1]:
        return 128.0
    hist = img.crop(box).convert("L").histogram()
    tot = sum(hist)
    return sum(i * c for i, c in enumerate(hist)) / tot if tot else 128.0


def compute_box(framed_size, frame_total, sig_size, pos, margin_px):
    fw, fh = framed_size
    sw, sh = sig_size
    if pos[0] == "t":
        y0 = frame_total + margin_px
    else:
        y0 = fh - frame_total - margin_px - sh
    if pos[1] == "l":
        x0 = frame_total + margin_px
    elif pos[1] == "c":
        x0 = (fw - sw) // 2
    else:
        x0 = fw - frame_total - margin_px - sw
    return (x0, y0, x0 + sw, y0 + sh)


AUTO_CHOICES = [("white", (255, 255, 255)), ("gray", (160, 160, 160)), ("black", (0, 0, 0))]


def best_auto_color(bg):
    return max(AUTO_CHOICES, key=lambda o: abs(o[1][0] - bg))


def lum_of(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def choose(framed, frame_total, sig_size, margin_px, P):
    """Renvoie (pos, rgb, luminosite_fond)."""
    pos = P.get("sig_pos", "auto")
    auto_color = P.get("sig_color_auto", False)
    fixed = hex_rgb(P.get("sig_color", "#a0a0a0"), (160, 160, 160))
    cands = [pos] if pos != "auto" else ["bl", "br"]
    res = []
    for c in cands:
        bg = region_luminance(framed, compute_box(framed.size, frame_total, sig_size, c, margin_px))
        if auto_color:
            _, rgb = best_auto_color(bg)
        else:
            rgb = fixed
        res.append((c, rgb, bg, abs(lum_of(rgb) - bg)))
    if len(res) == 1:
        return res[0][:3]
    left, right = res
    if left[3] >= CONTRAST_GOOD_ENOUGH or right[3] <= left[3]:
        return left[:3]
    return right[:3]


def apply_signature(framed, P, frame_total, margin_px, sig_w):
    mask = build_mask(P, sig_w)
    sig_size = mask.size
    pos, rgb, bg = choose(framed, frame_total, sig_size, margin_px, P)
    opacity = max(0.0, min(1.0, float(P.get("sig_opacity", 100)) / 100.0))
    if opacity < 1.0:
        mask = mask.point(lambda v: int(v * opacity))
    box = compute_box(framed.size, frame_total, sig_size, pos, margin_px)
    if P.get("sig_shadow"):
        off = max(1, round(sig_size[0] * 0.012))
        sh_mask = mask.filter(ImageFilter.GaussianBlur(max(1, off)))
        sh_mask = sh_mask.point(lambda v: int(v * 0.6))
        dark = Image.new("RGB", sig_size, (0, 0, 0))
        framed.paste(dark, (box[0] + off, box[1] + off), sh_mask)
    layer = Image.new("RGB", sig_size, rgb)
    framed.paste(layer, (box[0], box[1]), mask)
    return framed, pos, rgb, bg


def process_image(img_rgb, P):
    """Applique redimensionnement + cadre + signature. Renvoie (image, statut)."""
    if P.get("resize_on"):
        long_side = max(img_rgb.size)
        mx = max(100, int(P.get("resize_max", 2480)))
        if long_side > mx:
            s = mx / long_side
            img_rgb = img_rgb.resize((max(1, round(img_rgb.width * s)), max(1, round(img_rgb.height * s))),
                                     Image.LANCZOS)
    if P.get("frame_on"):
        framed, frame_total = add_frame(img_rgb, P)
    else:
        framed, frame_total = img_rgb.copy(), 0
    statut = "OK"
    if P.get("sig_on"):
        margin_px = round(min(img_rgb.size) * float(P.get("sig_margin", 0.3)) / 100.0)
        # taille proportionnelle au PETIT cote : identique en paysage et en portrait
        sig_w = max(2, round(min(img_rgb.size) * float(P.get("sig_size", 20)) / 100.0))
        framed, pos, rgb, bg = apply_signature(framed, P, frame_total, margin_px, sig_w)
        names = {"bl": "bas gauche", "br": "bas droite", "bc": "bas centre",
                 "tl": "haut gauche", "tr": "haut droite", "tc": "haut centre"}
        statut = f"OK - signature {names.get(pos, pos)} (fond {bg:.0f}/255)"
    return framed, statut


# ---------------------------------------------------------------- traitement
STATE_LOCK = threading.Lock()
STATE = {"running": False, "total": 0, "done": 0, "rows": [], "log": [],
         "finished_ok": 0, "stop": False, "stopped": False}


def _log(msg):
    with STATE_LOCK:
        STATE["log"].append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
        STATE["log"] = STATE["log"][-200:]


def _media_scan(path):
    """Previent la galerie d'Android qu'une nouvelle photo existe."""
    try:
        from java import jclass
        ctx = jclass("android.app.ActivityThread").currentApplication()
        jclass("android.media.MediaScannerConnection").scanFile(ctx, [path], None, None)
    except Exception:
        pass


def open_oriented(path):
    """Ouvre la photo, la redresse selon l'EXIF et renvoie (rgb, exif_bytes_sans_rotation)."""
    with Image.open(path) as im:
        exif = im.getexif()
        exif_bytes = im.info.get("exif")
        rgb = ImageOps.exif_transpose(im).convert("RGB")
    if exif_bytes:
        try:
            exif[0x0112] = 1
            exif_bytes = exif.tobytes()
        except Exception:
            pass
    return rgb, exif_bytes


def run_batch(paths, names, P):
    out_dir = P.get("out_folder") or "/storage/emulated/0/Pictures/AVEC_CADRE"
    n_total = len(paths)
    with STATE_LOCK:
        STATE.update(total=n_total, rows=[], done=0)
    try:
        os.makedirs(out_dir, exist_ok=True)
    except Exception as e:
        _log(f"Impossible de creer le dossier {out_dir} : {e}")
        with STATE_LOCK:
            STATE["running"] = False
        return
    _log(f"{n_total} photo(s) recue(s) -> {out_dir}")
    n_ok, stopped = 0, False
    quality = max(50, min(100, int(P.get("quality", 95))))
    for i, (path, fname) in enumerate(zip(paths, names), start=1):
        with STATE_LOCK:
            must_stop = STATE["stop"]
        if must_stop:
            stopped = True
            try:
                os.remove(path)
            except OSError:
                pass
            continue
        try:
            img, exif_bytes = open_oriented(path)
            framed, statut = process_image(img, P)
            tags = []
            if P.get("resize_on"):
                tags.append("WEB")
            if P.get("frame_on") or P.get("sig_on"):
                tags.append("CADRE")
            suffix = "_" + "_".join(tags) if tags else "_TRAITE"
            base, ext = os.path.splitext(fname)
            if ext.lower() not in IMG_EXTENSIONS:
                ext = ".jpg"
            target = os.path.join(out_dir, f"{base}{suffix}{ext}")
            n = 1
            while os.path.exists(target):
                target = os.path.join(out_dir, f"{base}{suffix}_{n}{ext}")
                n += 1
            kw = {}
            if ext.lower() in (".jpg", ".jpeg"):
                kw["quality"] = quality
                if exif_bytes and P.get("keep_exif", True):
                    kw["exif"] = exif_bytes
            framed.save(target, **kw)
            _media_scan(target)
            n_ok += 1
            with STATE_LOCK:
                STATE["rows"].append({"n": i, "fichier": fname, "statut": statut,
                                      "nouveau_nom": os.path.basename(target)})
                STATE["done"] = i
        except Exception as e:
            _log(f"ERREUR sur {fname} : {e}")
            with STATE_LOCK:
                STATE["rows"].append({"n": i, "fichier": fname, "statut": f"ERREUR : {e}", "nouveau_nom": "-"})
                STATE["done"] = i
        finally:
            try:
                os.remove(path)
            except OSError:
                pass
    _log(("ARRETE par toi. " if stopped else "Termine. ") + f"{n_ok} photo(s) sur {n_total} -> {out_dir}")
    with STATE_LOCK:
        STATE.update(running=False, finished_ok=n_ok, stopped=stopped)


# ---------------------------------------------------------------- web
app = Flask(__name__)


def _params():
    try:
        return json.loads(request.form.get("params", "{}"))
    except Exception:
        return {}


@app.route("/")
def index():
    return Response(PAGE, mimetype="text/html")


@app.route("/fonts")
def fonts():
    return jsonify(list(list_fonts().keys()))


@app.route("/preview", methods=["POST"])
def preview():
    f = request.files.get("photo")
    if not f:
        return ("", 400)
    try:
        P = _params()
        with Image.open(f.stream) as im:
            img = ImageOps.exif_transpose(im).convert("RGB")
        img.thumbnail((1100, 1100), Image.LANCZOS)
        out, _ = process_image(img, P)
        out.thumbnail((1100, 1100), Image.LANCZOS)
        buf = io.BytesIO()
        out.save(buf, "JPEG", quality=85)
        return Response(buf.getvalue(), mimetype="image/jpeg")
    except Exception as e:
        return Response(str(e), status=500)


@app.route("/start_upload", methods=["POST"])
def start_upload():
    files = request.files.getlist("photos")
    if not files:
        return jsonify({"error": "Aucune photo recue."}), 400
    with STATE_LOCK:
        if STATE["running"]:
            return jsonify({"error": "Un traitement est deja en cours."}), 400
        STATE.update(running=True, stop=False, stopped=False, finished_ok=0, log=[], rows=[], done=0, total=0)
    P = _params()
    tmp = tempfile.mkdtemp(prefix="cadre_upload_")
    paths, names = [], []
    for i, f in enumerate(files):
        name = os.path.basename(f.filename) or f"photo_{i}.jpg"
        p = os.path.join(tmp, f"{i}_{name}")
        f.save(p)
        paths.append(p)
        names.append(name)
    threading.Thread(target=run_batch, args=(paths, names, P), daemon=True).start()
    return jsonify({"ok": True})


@app.route("/stop", methods=["POST"])
def stop():
    with STATE_LOCK:
        STATE["stop"] = True
    return jsonify({"ok": True})


@app.route("/status")
def status():
    with STATE_LOCK:
        return jsonify({"running": STATE["running"], "total": STATE["total"], "done": STATE["done"],
                        "rows": STATE["rows"], "log": STATE["log"], "ok": STATE["finished_ok"],
                        "stopped": STATE["stopped"]})


_SERVER = None


def start(port=8855):
    """Appele par l'appli Android : lance le serveur local en arriere-plan."""
    global _SERVER
    if _SERVER is None:
        _SERVER = make_server("127.0.0.1", int(port), app, threaded=True)
        threading.Thread(target=_SERVER.serve_forever, daemon=True).start()
    return port


from page import PAGE  # noqa: E402  (interface, voir page.py)

if __name__ == "__main__":
    start(8855)
    print("CADRE + SIGNATURE : http://127.0.0.1:8855")
    threading.Event().wait()
