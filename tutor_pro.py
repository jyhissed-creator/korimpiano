<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>KORYM Piano Virtual</title>
<style>
body {
  margin: 0;
  background: #0d0d0d;
  color: white;
  font-family: Arial, sans-serif;
}
header {
  padding: 10px;
  text-align: center;
  background: #111;
}
input, textarea, button, select {
  width: 100%;
  margin: 5px 0;
  padding: 8px;
  background: #222;
  color: white;
  border: none;
}
button {
  background: #6a00ff;
  cursor: pointer;
}
.container {
  display: flex;
  gap: 10px;
  padding: 10px;
}
.panel {
  width: 30%;
}
.piano-container {
  width: 70%;
}
#piano {
  display: flex;
  position: relative;
  height: 220px;
  margin-top: 20px;
}
.white {
  width: 40px;
  height: 220px;
  background: white;
  border: 1px solid #000;
  position: relative;
}
.black {
  width: 26px;
  height: 140px;
  background: black;
  position: absolute;
  top: 0;
  right: -13px;
  z-index: 2;
}
.left {
  background: #3cff0066 !important;
}
.right {
  background: #0099ff88 !important;
}
footer {
  text-align: center;
  font-size: 12px;
  opacity: 0.6;
}
</style>
</head>

<body>

<header>
<h2>🎹 KORYM Piano Virtual – Aprende con Canciones</h2>
</header>

<div class="container">

<div class="panel">
<label>🔗 URL de YouTube</label>
<input id="yt" placeholder="Pega el link aquí">

<label>🎼 Letra + Acordes</label>
<textarea id="lyrics" rows="10">
Coro:
F  Bb   C
Gracias Señor quiero darte
Am   Dm
Toda mi vida entregarte
</textarea>

<label>🎹 Tonalidad</label>
<select id="key">
<option>C</option><option>D</option><option>E</option>
<option>F</option><option>G</option><option>A</option><option>B</option>
</select>

<label>⏱ Velocidad</label>
<select id="speed">
<option value="1">Normal</option>
<option value="0.75">Lento</option>
<option value="0.5">Muy lento</option>
</select>

<button onclick="startLesson()">▶ Iniciar enseñanza</button>
</div>

<div class="piano-container">
<div id="piano"></div>
<iframe id="video" width="100%" height="250" style="margin-top:10px;border:none;"></iframe>
</div>

</div>

<footer>
KORYM Piano Virtual – Aprendizaje visual + audio 🎶
</footer>

<script>
const notes = [
"C","D","E","F","G","A","B",
"C2","D2","E2","F2","G2","A2","B2"
];

const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
const piano = document.getElementById("piano");
let keys = {};

notes.forEach(n => {
  const key = document.createElement("div");
  key.className = "white";
  key.dataset.note = n;
  key.onclick = () => play(n);
  piano.appendChild(key);
  keys[n] = key;
});

function freq(note) {
  const map = {
    C:261.6,D:293.7,E:329.6,F:349.2,G:392,A:440,B:493.9,
    C2:523.3,D2:587.3,E2:659.3,F2:698.4,G2:784,A2:880,B2:987.8
  };
  return map[note];
}

function play(note) {
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();
  osc.frequency.value = freq(note);
  osc.type = "sine";
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start();
  gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 1);
}

function highlight(note, hand) {
  keys[note].classList.add(hand);
  play(note);
  setTimeout(() => keys[note].classList.remove(hand), 600);
}

function startLesson() {
  const speed = parseFloat(document.getElementById("speed").value);
  const url = document.getElementById("yt").value;
  if (url) {
    document.getElementById("video").src =
      "https://www.youtube.com/embed/" + url.split("v=")[1];
  }

  let seq = [
    {n:"C",h:"left"},
    {n:"G",h:"right"},
    {n:"E",h:"right"},
    {n:"F",h:"left"},
    {n:"A",h:"right"},
  ];

  seq.forEach((s,i) => {
    setTimeout(() => highlight(s.n, s.h), i * 1000 * speed);
  });
}
</script>

</body>
</html>
