<!DOCTYPE html>  <html lang="es">  
<head>  
<meta charset="UTF-8">  
<title>KORYM Piano Virtual IA</title>  
<script src="https://unpkg.com/tone@14.8.49/build/Tone.js"></script>  
<style>  
body{margin:0;background:#050008;color:#fff;font-family:Arial}  
header{padding:15px;text-align:center;font-size:24px;background:linear-gradient(90deg,#6a00ff,#9b4dff)}  
.main{padding:10px}  
.card{background:#0b0b0b;border-radius:14px;padding:12px;margin-bottom:10px}  
input,button{width:100%;padding:10px;border:none;border-radius:10px;background:#111;color:#fff;margin-bottom:8px}  
button{background:#6a00ff;font-size:18px}  
#estado{text-align:center}  
</style>  
</head>  <body>  
<header>🎹 KORYM Piano Virtual IA</header>  <div class="main">  
<div class="card">  
<input id="orden" placeholder="Ej: transponer a Re, más rápido">  
<button onclick="procesarOrden()">🧠 Orden</button>  
<button onclick="iniciar()">▶ Iniciar IA</button>  
<p id="estado">IA lista</p>  
</div>  <div class="card">  
<input type="file" id="mediaFile" accept="audio/*,video/*">  
<audio id="audioPlayer" controls></audio>  
</div>  
</div>  <script>  
/* ================= CEREBRO ================= */  
const NOTAS=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]  
const CEREBRO={  
estado:{bpm:90},  
memoria:{cancion:[]},  
ia:{acordes:[]}  
}  
  
/* ================= AUDIO ================= */  
let ctx, analyser, data  
async function iniciar(){  
await Tone.start()  
ctx = Tone.getContext().rawContext  
const stream = await navigator.mediaDevices.getUserMedia({audio:true})  
const mic = ctx.createMediaStreamSource(stream)  
analyser = ctx.createAnalyser()  
analyser.fftSize=2048  
data = new Float32Array(analyser.frequencyBinCount)  
mic.connect(analyser)  
analizarAudio()  
estado.innerText="🎧 Analizando canción completa…"  
}  
  
/* ================= IA CENTRAL ================= */  
function analizarAudio(){  
analyser.getFloatFrequencyData(data)  
  
const notasDetectadas = extraerNotas(data,ctx.sampleRate)  
if(notasDetectadas.length){  
const acorde = detectarAcorde(notasDetectadas)  
CEREBRO.memoria.cancion.push(notasDetectadas)  
if(acorde) CEREBRO.ia.acordes.push(acorde)  
estado.innerText="🎼 "+notasDetectadas.join(" ")+" | "+(acorde||"")  
}  
requestAnimationFrame(analizarAudio)  
}  
  
/* ================= POLIFONÍA HEURÍSTICA ================= */  
function extraerNotas(spec,sr){  
let notas=[]  
for(let i=5;i<300;i++){  
if(spec[i]>-40){  
let f=i*sr/2048  
let n=Math.round(12*Math.log2(f/440)+69)  
if(n>20&&n<100){  
let nota=NOTAS[n%12]  
if(!notas.includes(nota)) notas.push(nota)  
}  
}  
}  
return notas.slice(0,4) // hasta 4 notas simultáneas  
}  
  
/* ================= ACORDES ================= */  
function detectarAcorde(n){  
const s=n.sort().join("")  
if(s==="CEG")return"C"  
if(s==="DFA")return"Dm"  
if(s==="CEGB")return"Cmaj7"  
return null  
}  
  
/* ================= ÓRDENES ================= */  
function procesarOrden(){  
let t=orden.value.toLowerCase()  
if(t.includes("rápido"))CEREBRO.estado.bpm+=10  
if(t.includes("lento"))CEREBRO.estado.bpm-=10  
estado.innerText="⚙ BPM "+CEREBRO.estado.bpm  
}  
  
/* ================= MEDIA ================= */  
mediaFile.onchange=e=>{  
audioPlayer.src=URL.createObjectURL(e.target.files[0])  
audioPlayer.play()  
}  
</script>  </body>  
</html>
