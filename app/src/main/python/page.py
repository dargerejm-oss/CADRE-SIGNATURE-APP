# -*- coding: utf-8 -*-
PAGE = r'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cadre + Signature</title>
<style>
  *{box-sizing:border-box}
  body{font-family:Roboto,-apple-system,sans-serif;background:#0e0e12;color:#eee;margin:0;padding:12px 12px 120px;-webkit-tap-highlight-color:transparent}
  h1{font-size:1.45em;margin:2px 0 0;letter-spacing:.5px}
  .credit{color:#8a8a99;font-size:.75em;margin:2px 0 12px}
  .card{background:#1a1a22;border-radius:14px;padding:14px;margin-bottom:12px}
  label{display:block;margin:12px 0 5px;color:#b5b5c5;font-size:.9em}
  input[type=text],input[type=number],select{width:100%;padding:12px;border-radius:10px;border:1px solid #3a3a4a;background:#0b0b10;color:#fff;font-size:1em}
  input[type=color]{width:100%;height:46px;border:1px solid #3a3a4a;border-radius:10px;background:#0b0b10;padding:3px}
  input[type=range]{width:100%;height:34px;accent-color:#9b51e0}
  .row{display:flex;align-items:center;gap:10px;margin:10px 0;font-size:1.02em}
  .row input[type=checkbox]{width:26px;height:26px;accent-color:#27ae60;flex:none}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:8px}
  .grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px}
  .tabs{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-bottom:12px}
  .tab{border:none;border-radius:12px;padding:14px 2px;font-size:.78em;font-weight:bold;color:#fff;opacity:.45;line-height:1.25}
  .tab .ic{display:block;font-size:1.7em;margin-bottom:2px}
  .tab.on{opacity:1;box-shadow:0 0 0 3px #fff3 inset,0 3px 10px #0008;transform:translateY(-1px)}
  .t1{background:#2f80ed}.t2{background:#e67e22}.t3{background:#9b51e0}.t4{background:#00a0a0}.t5{background:#27ae60}
  .panel{display:none}.panel.on{display:block}
  .big{width:100%;border:none;border-radius:14px;padding:18px 10px;font-size:1.15em;font-weight:bold;color:#fff;margin:6px 0}
  .bluebtn{background:#2f80ed}
  .pack{border:none;border-radius:12px;padding:16px 6px;font-size:1em;font-weight:bold;color:#fff}
  .pk1{background:#333}.pk2{background:#e8e8e8;color:#111}.pk3{background:#b8902a}.pk4{background:#5b6b7d}
  .pos{border:2px solid #3a3a4a;background:#0b0b10;color:#bbb;border-radius:10px;padding:15px 0;font-size:.95em;font-weight:bold}
  .pos.on{background:#9b51e0;border-color:#c79bff;color:#fff}
  .sw{display:flex;flex-wrap:wrap;gap:10px;margin:8px 0}
  .sw span{width:38px;height:38px;border-radius:50%;border:3px solid #555;display:inline-block}
  .sw span.on{border-color:#fff;box-shadow:0 0 0 3px #9b51e0}
  #preview{background:#000;border-radius:12px;min-height:60px;text-align:center;overflow:hidden;position:relative}
  #prevImg{max-width:100%;max-height:42vh;display:none;margin:0 auto}
  #prevMsg{color:#8a8a99;font-size:.9em;padding:18px 10px}
  #prevBusy{position:absolute;top:8px;right:10px;font-size:.8em;color:#fff;background:#0009;border-radius:8px;padding:3px 8px;display:none}
  .val{color:#fff;font-weight:bold}
  #doneBanner{display:none;background:#1faa4b;color:#fff;font-weight:bold;font-size:2.2em;text-align:center;padding:24px 8px;border-radius:14px;margin-bottom:12px;letter-spacing:2px}
  #msgBox{display:none;background:#7a2b2b;color:#fff;padding:12px;border-radius:10px;margin-bottom:12px}
  #progressWrap{background:#2a2a35;border-radius:10px;height:34px;overflow:hidden;margin-top:6px}
  #progressBar{background:linear-gradient(90deg,#27ae60,#58d68d);height:100%;width:0%;transition:width .2s}
  #progressLabel{text-align:center;font-size:1.1em;font-weight:bold;margin-top:8px}
  #log{background:#000;padding:8px;border-radius:8px;font-family:monospace;font-size:.72em;height:110px;overflow-y:auto;margin-top:10px;white-space:pre-wrap}
  table{width:100%;border-collapse:collapse;font-size:.8em;margin-top:10px}
  td{border-bottom:1px solid #2d2d3a;padding:5px 3px}
  .ok{color:#5fd67a}.err{color:#e05a5a}
  #bar{position:fixed;left:0;right:0;bottom:0;background:#0e0e12ee;padding:10px 12px 14px;display:grid;grid-template-columns:1fr;gap:8px;border-top:1px solid #2a2a35}
  #launchBtn{background:#27ae60;font-size:1.3em;padding:20px 8px;margin:0}
  #launchBtn:disabled{background:#555}
  #stopBtn{display:none;background:#c0392b;font-size:1.2em;padding:16px;margin:0}
  .hint{color:#8a8a99;font-size:.8em;margin-top:6px}
  .hide{display:none}
</style>
</head>
<body>
<h1>📷 Cadre + Signature</h1>
<div class="credit">JM.DARGERE &middot; @jean_michel_dargere</div>

<div id="doneBanner">TERMIN&Eacute;</div>
<div id="msgBox"></div>

<div class="card" style="padding:10px">
  <div id="preview"><div id="prevMsg">Choisis une photo (onglet PHOTOS) pour voir l'aper&ccedil;u ici.</div><img id="prevImg" alt=""><div id="prevBusy">&hellip;</div></div>
</div>

<div class="tabs">
  <button class="tab t1 on" data-p="p1"><span class="ic">🖼️</span>PHOTOS</button>
  <button class="tab t2" data-p="p2"><span class="ic">🔲</span>CADRE</button>
  <button class="tab t3" data-p="p3"><span class="ic">✍️</span>SIGNATURE</button>
  <button class="tab t4" data-p="p4"><span class="ic">⚙️</span>OPTIONS</button>
  <button class="tab t5" data-p="p5"><span class="ic">✅</span>R&Eacute;SULTAT</button>
</div>

<!-- ============ PHOTOS ============ -->
<div class="panel on" id="p1">
  <div class="card">
    <input type="file" id="photoFiles" multiple accept="image/*" class="hide">
    <button class="big bluebtn" onclick="document.getElementById('photoFiles').click()">📂 CHOISIR MES PHOTOS</button>
    <div id="fileCount" class="hint" style="font-size:1em">Aucune photo s&eacute;lectionn&eacute;e</div>
    <label>Dossier de sortie (visible dans ta galerie)</label>
    <input type="text" id="out_folder">
  </div>
  <div class="card">
    <div style="font-weight:bold;margin-bottom:8px">🎨 Styles pr&ecirc;ts &agrave; l'emploi</div>
    <div class="grid2">
      <button class="pack pk1" onclick="pack('classic')">Classique noir</button>
      <button class="pack pk2" onclick="pack('gallery')">Galerie blanc</button>
      <button class="pack pk3" onclick="pack('gold')">Dor&eacute;</button>
      <button class="pack pk4" onclick="pack('discret')">Discret</button>
    </div>
    <div class="hint">Un style change le cadre et la signature d'un coup. Tu peux ensuite tout ajuster.</div>
  </div>
</div>

<!-- ============ CADRE ============ -->
<div class="panel" id="p2">
  <div class="card">
    <div class="row"><input type="checkbox" id="frame_on"><span><b>Ajouter le cadre</b></span></div>
    <label>Style du cadre</label>
    <select id="frame_style">
      <option value="classic">Noir classique (liser&eacute; blanc)</option>
      <option value="white">Blanc (liser&eacute; noir)</option>
      <option value="custom">Couleurs libres</option>
    </select>
    <div id="customFrame" class="hide">
      <div class="grid3">
        <div><label>Ext&eacute;rieur</label><input type="color" id="frame_outer"></div>
        <div><label>Liser&eacute;</label><input type="color" id="frame_line"></div>
        <div><label>Int&eacute;rieur</label><input type="color" id="frame_inner"></div>
      </div>
    </div>
    <label>&Eacute;paisseur du cadre : <span class="val" id="frame_thick_v"></span> %</label>
    <input type="range" id="frame_thick" min="30" max="300" step="5">
  </div>
</div>

<!-- ============ SIGNATURE ============ -->
<div class="panel" id="p3">
  <div class="card">
    <div class="row"><input type="checkbox" id="sig_on"><span><b>Ajouter la signature</b></span></div>
    <label>Type de signature</label>
    <select id="sig_kind">
      <option value="initials">Initiales (JM D) &mdash; discret</option>
      <option value="full">Compl&egrave;te (JM.Dargere)</option>
      <option value="text">Mon propre texte</option>
    </select>
    <div id="textOpts" class="hide">
      <label>Texte</label>
      <input type="text" id="sig_text">
      <label>Police</label>
      <select id="sig_font"></select>
    </div>
  </div>

  <div class="card">
    <div style="font-weight:bold">🎨 Couleur</div>
    <div class="row"><input type="checkbox" id="sig_color_auto"><span>Automatique (blanc / gris / noir selon la photo)</span></div>
    <div class="sw" id="swatches"></div>
    <label>Autre couleur</label>
    <input type="color" id="sig_color">
    <label>Transparence : <span class="val" id="sig_opacity_v"></span> % opaque</label>
    <input type="range" id="sig_opacity" min="10" max="100" step="5">
    <div class="row"><input type="checkbox" id="sig_shadow"><span>Ombre l&eacute;g&egrave;re (lisible sur fond charg&eacute;)</span></div>
  </div>

  <div class="card">
    <div style="font-weight:bold;margin-bottom:8px">📍 Position</div>
    <button class="pos" id="posAuto" data-pos="auto" style="width:100%;margin-bottom:8px">AUTOMATIQUE (gauche ou droite, la mieux contrast&eacute;e)</button>
    <div class="grid3">
      <button class="pos" data-pos="tl">&#8598; Haut gauche</button>
      <button class="pos" data-pos="tc">&#8593; Haut centre</button>
      <button class="pos" data-pos="tr">&#8599; Haut droite</button>
      <button class="pos" data-pos="bl">&#8601; Bas gauche</button>
      <button class="pos" data-pos="bc">&#8595; Bas centre</button>
      <button class="pos" data-pos="br">&#8600; Bas droite</button>
    </div>
    <label>Taille (<span id="sizeKind"></span>) : <span class="val" id="sig_size_v"></span> % du petit c&ocirc;t&eacute; de la photo</label>
    <input type="range" id="sig_size" min="1" max="50" step="0.5">
    <div class="hint">Proportionnelle au petit c&ocirc;t&eacute; : m&ecirc;me taille visuelle en paysage et en portrait. Chaque type a sa propre taille par d&eacute;faut.</div>
    <label>Distance au bord : <span class="val" id="sig_margin_v"></span> %</label>
    <input type="range" id="sig_margin" min="-1.5" max="4" step="0.05">
  </div>
</div>

<!-- ============ OPTIONS ============ -->
<div class="panel" id="p4">
  <div class="card">
    <div class="row"><input type="checkbox" id="resize_on"><span>Redimensionner (web / t&eacute;l&eacute;phone)</span></div>
    <label>Plus grand c&ocirc;t&eacute; maximum (pixels)</label>
    <input type="number" id="resize_max" inputmode="numeric">
    <label>Qualit&eacute; JPEG : <span class="val" id="quality_v"></span> %</label>
    <input type="range" id="quality" min="60" max="100" step="1">
    <div class="row"><input type="checkbox" id="keep_exif"><span>Garder les infos de la photo (EXIF, date, GPS)</span></div>
    <div class="hint">Les photos prises en portrait sont automatiquement remises dans le bon sens avant le cadre.</div>
  </div>
  <div class="card">
    <button class="big" style="background:#555" onclick="resetAll()">↺ Revenir aux r&eacute;glages d'origine</button>
  </div>
</div>

<!-- ============ RESULTAT ============ -->
<div class="panel" id="p5">
  <div class="card">
    <div id="progressWrap"><div id="progressBar"></div></div>
    <div id="progressLabel">En attente</div>
    <div id="log"></div>
    <table id="resultsTable"><tbody></tbody></table>
  </div>
</div>

<div id="bar">
  <button class="big" id="launchBtn" onclick="lancer()">▶ LANCER</button>
  <button class="big" id="stopBtn" onclick="arreter()">■ STOP</button>
</div>

<script>
const $ = id => document.getElementById(id);
const DEF = {
  out_folder:'/storage/emulated/0/Pictures/AVEC_CADRE',
  frame_on:true, frame_style:'classic', frame_outer:'#000000', frame_line:'#ffffff', frame_inner:'#000000', frame_thick:100,
  sig_on:true, sig_kind:'initials', sig_text:'JM.Dargère', sig_font:'',
  sig_color_auto:false, sig_color:'#a0a0a0', sig_opacity:100, sig_shadow:false,
  sig_pos:'auto', sig_size_initials:22, sig_size_full:25, sig_size_text:22, sig_margin:0.3,
  resize_on:false, resize_max:2480, quality:95, keep_exif:true
};
const SWATCH = ['#ffffff','#000000','#a0a0a0','#d4af37','#e74c3c','#f39c12','#2ecc71','#3498db','#9b59b6','#ff69b4'];
let S = Object.assign({}, DEF);
try{ Object.assign(S, JSON.parse(localStorage.getItem('cadre_v2')||'{}')); }catch(e){}
const KEYS = Object.keys(DEF).filter(k=>k!=='sig_pos' && k.indexOf('sig_size_')!==0);
const KIND_NAMES={initials:'initiales',full:'complète',text:'texte'};
function sizeKey(){ return 'sig_size_'+S.sig_kind; }
function params(){ return Object.assign({}, S, {sig_size: parseFloat(S[sizeKey()])}); }
let FILES = [], previewBlob = null, previewSeq = 0, previewTimer = null, polling = null;

function save(){ try{ localStorage.setItem('cadre_v2', JSON.stringify(S)); }catch(e){} }
function msg(t){ const b=$('msgBox'); b.innerText=t; b.style.display=t?'block':'none'; if(t) window.scrollTo(0,0); }

function syncUI(){
  KEYS.forEach(k=>{
    const el=$(k); if(!el) return;
    if(el.type==='checkbox') el.checked=!!S[k]; else el.value=S[k];
    const v=$(k+'_v'); if(v) v.innerText=S[k];
  });
  $('sig_size').value=S[sizeKey()]; $('sig_size_v').innerText=S[sizeKey()]; $('sizeKind').innerText=KIND_NAMES[S.sig_kind]||'';
  document.querySelectorAll('.pos').forEach(b=>b.classList.toggle('on', b.dataset.pos===S.sig_pos));
  $('customFrame').classList.toggle('hide', S.frame_style!=='custom');
  $('textOpts').classList.toggle('hide', S.sig_kind!=='text');
  $('sig_color').disabled = !!S.sig_color_auto;
  document.querySelectorAll('#swatches span').forEach(s=>s.classList.toggle('on', !S.sig_color_auto && s.dataset.c===S.sig_color.toLowerCase()));
}

$('sig_size').addEventListener('input',()=>{ S[sizeKey()]=$('sig_size').value; syncUI(); save(); schedulePreview(); });
KEYS.forEach(k=>{
  const el=$(k); if(!el) return;
  const h=()=>{ S[k]= el.type==='checkbox' ? el.checked : el.value; syncUI(); save(); schedulePreview(); };
  el.addEventListener('input',h); el.addEventListener('change',h);
});
document.querySelectorAll('.pos').forEach(b=>b.onclick=()=>{ S.sig_pos=b.dataset.pos; syncUI(); save(); schedulePreview(); });
SWATCH.forEach(c=>{ const s=document.createElement('span'); s.style.background=c; s.dataset.c=c;
  s.onclick=()=>{ S.sig_color=c; S.sig_color_auto=false; syncUI(); save(); schedulePreview(); }; $('swatches').appendChild(s); });
document.querySelectorAll('.tab').forEach(t=>t.onclick=()=>showTab(t.dataset.p));
function showTab(p){
  document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('on', t.dataset.p===p));
  document.querySelectorAll('.panel').forEach(x=>x.classList.toggle('on', x.id===p));
  window.scrollTo(0,0);
}

const PACKS = {
  classic:{frame_on:true,frame_style:'classic',frame_thick:100,sig_on:true,sig_kind:'initials',sig_color_auto:false,sig_color:'#a0a0a0',sig_opacity:100,sig_shadow:false},
  gallery:{frame_on:true,frame_style:'white',frame_thick:120,sig_on:true,sig_kind:'full',sig_color_auto:true,sig_opacity:100,sig_shadow:false},
  gold:{frame_on:true,frame_style:'custom',frame_outer:'#16130c',frame_line:'#d4af37',frame_inner:'#16130c',frame_thick:110,sig_on:true,sig_kind:'full',sig_color_auto:false,sig_color:'#d4af37',sig_opacity:100,sig_shadow:true},
  discret:{frame_on:true,frame_style:'classic',frame_thick:60,sig_on:true,sig_kind:'initials',sig_color_auto:false,sig_color:'#ffffff',sig_opacity:70,sig_shadow:false}
};
function pack(n){ Object.assign(S, PACKS[n]); syncUI(); save(); schedulePreview(); }
function resetAll(){ S=Object.assign({},DEF); syncUI(); save(); schedulePreview(); }

// ---- polices
fetch('/fonts').then(r=>r.json()).then(list=>{
  const sel=$('sig_font'); sel.innerHTML='';
  (list.length?list:['(police par defaut)']).forEach(n=>{ const o=document.createElement('option'); o.value=n; o.textContent=n; sel.appendChild(o); });
  if(!S.sig_font || list.indexOf(S.sig_font)<0) S.sig_font=sel.options[0].value;
  sel.value=S.sig_font; save(); schedulePreview();
}).catch(()=>{});

// ---- fichiers + apercu
$('photoFiles').addEventListener('change', async function(){
  FILES = Array.from(this.files);
  $('fileCount').innerText = FILES.length ? (FILES.length+' photo(s) sélectionnée(s)') : 'Aucune photo sélectionnée';
  previewBlob = null;
  if(FILES.length){
    try{
      const bmp = await createImageBitmap(FILES[0]);
      const sc = Math.min(1, 1400/Math.max(bmp.width,bmp.height));
      const c = document.createElement('canvas'); c.width=Math.round(bmp.width*sc); c.height=Math.round(bmp.height*sc);
      c.getContext('2d').drawImage(bmp,0,0,c.width,c.height);
      previewBlob = await new Promise(r=>c.toBlob(r,'image/jpeg',0.9));
    }catch(e){ previewBlob = FILES[0]; }
  }
  schedulePreview();
});
function schedulePreview(){ clearTimeout(previewTimer); previewTimer=setTimeout(doPreview,350); }
function doPreview(){
  if(!previewBlob){ return; }
  const seq=++previewSeq; $('prevBusy').style.display='block';
  const fd=new FormData(); fd.append('photo', previewBlob, 'p.jpg'); fd.append('params', JSON.stringify(params()));
  fetch('/preview',{method:'POST',body:fd}).then(r=>{ if(!r.ok) throw new Error('apercu'); return r.blob(); }).then(b=>{
    if(seq!==previewSeq) return;
    const old=$('prevImg').src; $('prevImg').src=URL.createObjectURL(b); if(old.startsWith('blob:')) URL.revokeObjectURL(old);
    $('prevImg').style.display='block'; $('prevMsg').style.display='none'; $('prevBusy').style.display='none';
  }).catch(()=>{ if(seq===previewSeq) $('prevBusy').style.display='none'; });
}

// ---- fin visible
function beep(){
  try{ const C=new (window.AudioContext||window.webkitAudioContext)();
    [880,1175,1568].forEach((f,k)=>{ const o=C.createOscillator(),g=C.createGain(); o.frequency.value=f; o.connect(g); g.connect(C.destination);
      g.gain.setValueAtTime(0.25,C.currentTime+k*0.18); o.start(C.currentTime+k*0.18); o.stop(C.currentTime+k*0.18+0.15); }); }catch(e){}
  try{ if(navigator.vibrate) navigator.vibrate([200,100,200,100,400]); }catch(e){}
}
function arreter(){ fetch('/stop',{method:'POST'}); $('stopBtn').innerText='Arrêt en cours…'; }

function lancer(){
  msg(''); $('doneBanner').style.display='none';
  if(!FILES.length){ showTab('p1'); msg("Choisis d'abord au moins une photo dans la galerie."); return; }
  if(!S.out_folder.trim()){ showTab('p1'); msg("Indique un dossier de sortie."); return; }
  if(!S.frame_on && !S.sig_on && !S.resize_on){ msg("Coche au moins une option (cadre, signature ou redimensionnement)."); return; }
  const fd=new FormData(); FILES.forEach(f=>fd.append('photos',f)); fd.append('params', JSON.stringify(params()));
  $('launchBtn').disabled=true; $('stopBtn').style.display='block'; $('stopBtn').innerText='■ STOP';
  $('resultsTable').querySelector('tbody').innerHTML=''; $('log').innerText='Envoi des photos…'; $('progressBar').style.width='0%';
  showTab('p5');
  fetch('/start_upload',{method:'POST',body:fd}).then(r=>r.json()).then(d=>{
    if(d.error){ msg(d.error); $('launchBtn').disabled=false; $('stopBtn').style.display='none'; return; }
    polling=setInterval(poll,600);
  }).catch(e=>{ msg("Erreur d'envoi : "+e); $('launchBtn').disabled=false; $('stopBtn').style.display='none'; });
}
function poll(){
  fetch('/status').then(r=>r.json()).then(d=>{
    const pct=d.total?Math.round(100*d.done/d.total):0;
    $('progressBar').style.width=pct+'%'; $('progressLabel').innerText=d.done+' / '+d.total+'  ('+pct+' %)';
    $('log').innerText=d.log.join('\n'); $('log').scrollTop=$('log').scrollHeight;
    const tb=$('resultsTable').querySelector('tbody'); tb.innerHTML='';
    d.rows.slice(-30).reverse().forEach(row=>{ const tr=document.createElement('tr');
      const cls=row.statut.indexOf('ERREUR')>=0?'err':'ok';
      tr.innerHTML='<td>'+row.n+'</td><td>'+row.fichier+'</td><td class="'+cls+'">'+row.statut+'</td>'; tb.appendChild(tr); });
    if(!d.running){
      clearInterval(polling); $('launchBtn').disabled=false; $('stopBtn').style.display='none';
      const bn=$('doneBanner'); bn.style.background=d.stopped?'#d68910':'#1faa4b';
      bn.innerHTML=(d.stopped?'ARR&Ecirc;T&Eacute;':'TERMIN&Eacute;')+'<div style="font-size:.4em;font-weight:normal;margin-top:8px">'+d.ok+' photo(s) enregistrée(s) dans '+S.out_folder+'</div>';
      bn.style.display='block'; window.scrollTo(0,0); beep();
    }
  });
}
syncUI();
</script>
</body>
</html>
'''
