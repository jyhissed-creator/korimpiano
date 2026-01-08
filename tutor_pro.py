<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>KORYM Piano Maestro</title>
<style>
  body { margin: 0; background: #0d0d0d; color: white; font-family: 'Segoe UI', sans-serif; }
  header { padding: 15px; text-align: center; background: #1a1a1a; border-bottom: 2px solid #6a00ff; }
  
  .main-layout { display: flex; flex-direction: row; gap: 15px; padding: 15px; height: 90vh; }
  @media (max-width: 800px) { .main-layout { flex-direction: column; } }

  /* PANEL DE CONTROL */
  .panel { width: 320px; background: #181818; padding: 20px; border-radius: 15px; display: flex; flex-direction: column; gap: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
  label { font-size: 11px; color: #888; text-transform: uppercase; font-weight: bold; }
  input, textarea, select { background: #252525; color: white; border: 1px solid #333; padding: 10px; border-radius: 8px; width: 100%; box-sizing: border-box; }
  button { background: #6a00ff; color: white; border: none; padding: 15px; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; }
  button:hover { background: #822eff; transform: translateY(-2px); }

  /* AREA DEL PIANO */
  .work-area { flex-grow: 1; display: flex; flex-direction: column; gap: 15px; }
  .piano-wrapper { 
    background: #000; padding: 30px 10px; border-radius: 15px; overflow-x: auto; 
    border: 1px solid #333; position: relative;
  }
  #piano { display: flex; position: relative; width: 720px; height: 220px; margin: 0 auto; }

  /* TECLAS */
  .key { position: absolute; cursor: pointer; border-radius: 0 0 6px 6px; transition: 0.1s; user-select: none; }
  .white { width: 60px; height: 220px; background: white; border: 1px solid #ddd; z-index: 1; color: #999; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 10px; }
  .black { width: 36px; height: 130px; background: #222; border: 1px solid #000; position: absolute; z-index: 2; color: #fff; font-size: 10px; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 5px; }

  /* COLORES DE MANOS (TU DISEÑO) */
  .left { background: #3cff00 !important; box-shadow: 0 0 15px #3cff00; color: white !important; }
  .right { background: #0099ff !important; box-shadow: 0 0 15px #0099ff; color: white !important; }
</style>
</head>
<body>

<header>
  <strong>🎹 KORYM PIANO VIRTUAL</strong>
</header>

<div class="main-layout">
  <div class="panel">
    <label>🔗 Video de YouTube</label>
    <input id="yt" placeholder="Pega el link aquí" value="https://www.youtube.com/watch?v=Xyuuv5co7ko">
    
    <label>📝 Letra y Acordes</label>
    <textarea id="lyrics" rows="5">F  Bb  C&#10;Gracias Señor</textarea>
    
    <label>🎹 Transportar a:</label>
    <select id="key-shift">
      <option value="0">Tono Original</option>
      <option value="-2">Bajar 2 semitonos</option>
      <option value="2">Subir 2 semitonos</option>
    </select>

    <button onclick="startLesson()">▶ INICIAR CLASE</button>
  </div>

  <div class="work-area">
    <div class="piano-wrapper">
      <div id="piano"></div>
    </div>
    <iframe id="video" width="100%" height="250" style="border-radius:15px; border:none;" src=""></iframe>
  </div>
</div>

<script>
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
const pianoContainer = document.getElementById("piano");

// Configuración de notas (Blancas y Negras)
const pianoNotes = [
  {n:"C", t:"white"}, {n:"C#", t:"black"}, {n:"D", t:"white"}, {n:"D#", t:"black"},
  {n:"E", t:"white"}, {n:"F", t:"white"}, {n:"F#", t:"black"}, {n:"G", t:"white"},
  {n:"G#", t:"black"}, {n:"A", t:"white"}, {n:"A#", t:"black"}, {n:"B", t:"white"},
  {n:"C2", t:"white"}
];

let whiteKeyCount = 0;
pianoNotes.forEach(note => {
  const key = document.createElement("div");
  key.className = `key ${note.t}`;
  key.id = `note-${note.n}`;
  key.innerHTML = `<span>${note.n}</span>`;
  
  if(note.t === "white") {
    key.style.left = (whiteKeyCount * 60) + "px";
    whiteKeyCount++;
  } else {
    // Posiciona la tecla negra entre las blancas
    key.style.left = (whiteKeyCount * 60 - 18) + "px";
  }
  
  key.onmousedown = () => play(note.n);
  pianoContainer.appendChild(key);
});

function play(note) {
  const freqs = {C:261, "C#":277, D:293, "D#":311, E:329, F:349, "F#":370, G:392, "G#":415, A:440, "A#":466, B:493, C2:523};
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.type = "triangle";
  osc.frequency.value = freqs[note] || 440;
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 1);
}

function highlight(note, hand) {
  const el = document.getElementById(`note-${note}`);
  if(el) {
    el.classList.add(hand);
    play(note);
    setTimeout(() => el.classList.remove(hand), 700);
  }
}

function startLesson() {
  const url = document.getElementById("yt").value;
  if (url.includes("v=")) {
    document.getElementById("video").src = "https://www.youtube.com/embed/" + url.split("v=")[1] + "?autoplay=1";
  }

  // Ejemplo de secuencia: Bajo (Izq) y Acorde (Der)
  const steps = [
    {n:"F", h:"left"}, {n:"A", h:"right"}, {n:"C2", h:"right"},
    {n:"C", h:"left"}, {n:"G", h:"right"}, {n:"E", h:"right"}
  ];

  steps.forEach((s, i) => {
    setTimeout(() => highlight(s.n, s.h), i * 1000);
  });
}
</script>
</body>
</html>
