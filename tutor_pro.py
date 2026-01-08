import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORYM Piano Virtual IA")

# El código HTML/JS con TODA tu lógica de IA integrada
piano_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>KORYM Piano Virtual IA</title>
    <script src="https://unpkg.com/tone@14.8.49/build/Tone.js"></script>
    <style>
        body{margin:0;background:#050008;color:#fff;font-family:Arial}
        header{padding:15px;text-align:center;font-size:24px;background:linear-gradient(90deg,#6a00ff,#9b4dff)}
        .main{padding:10px; display: flex; flex-direction: column; align-items: center;}
        .card{background:#0b0b0b;border-radius:14px;padding:12px;margin-bottom:10px; width: 95%; max-width: 800px;}
        input,button{width:100%;padding:10px;border:none;border-radius:10px;background:#111;color:#fff;margin-bottom:8px; box-sizing: border-box;}
        button{background:#6a00ff;font-size:18px; cursor: pointer;}
        #estado{text-align:center; color: #00ff88; min-height: 24px;}
        #piano{display:flex;justify-content:center;margin-top:15px;height:220px; position: relative;}
        .white{width:42px;height:220px;background:#fff;border:1px solid #000;position:relative; border-radius: 0 0 5px 5px;}
        .black{width:26px;height:140px;background:#000;position:absolute;top:0;right:-13px; z-index: 10; border-radius: 0 0 3px 3px;}
        .left-active{background:#00ff8855!important; box-shadow: 0 0 15px #00ff88;}
        .right-active{background:#00aaff88!important; box-shadow: 0 0 15px #00aaff;}
        audio{width:100%;margin-top:10px}
    </style>
</head>
<body>
    <header>🎹 KORYM Piano Virtual IA</header>
    <div class="main">
        <div class="card">
            <input id="orden" placeholder="Ej: transponer a Re, más rápido, enseñar">
            <button onclick="procesarOrden()">🧠 Enviar orden</button>
            <button onclick="iniciar()">▶ Iniciar IA</button>
            <p id="estado">IA lista para escuchar</p>
        </div>
        <div class="card">
            <input type="file" id="mediaFile" accept="audio/*,video/*">
            <audio id="audioPlayer" controls></audio>
        </div>
        <div id="piano"></div>
    </div>

<script>
/* ================= CEREBRO IA (TU INVENCIÓN) ================= */
const NOTAS = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"];
const CEREBRO = {
    estado: { tonalidad: "C", bpm: 90 },
    memoria: { original: [{nota:"C4",dur:"4n"},{nota:"E4",dur:"4n"},{nota:"G4",dur:"2n"}], actual: [] },
    oido: { ultimaNota: null },
    ia: { acordes: [] }
};
CEREBRO.memoria.actual = [...CEREBRO.memoria.original];

/* ================= GENERAR TECLADO ================= */
const pianoDiv = document.getElementById("piano");
for(let i=0; i<14; i++) {
    const n = NOTAS[i%12];
    const key = document.createElement("div");
    key.className = "white";
    key.id = "key-" + n + (i < 12 ? "4" : "5");
    if(["C","D","F","G","A"].includes(n)) {
        const b = document.createElement("div");
        b.className = "black";
        b.id = "key-" + n + "#" + (i < 12 ? "4" : "5");
        key.appendChild(b);
    }
    pianoDiv.appendChild(key);
}

/* ================= AUDIO Y OÍDO ================= */
let ctx, analyser, data;
let synth = new Tone.Synth().toDestination();

async function iniciar(){
    await Tone.start();
    ctx = Tone.getContext().rawContext;
    const stream = await navigator.mediaDevices.getUserMedia({audio:true});
    const mic = ctx.createMediaStreamSource(stream);
    analyser = ctx.createAnalyser();
    analyser.fftSize = 2048;
    data = new Float32Array(analyser.frequencyBinCount);
    mic.connect(analyser);
    analizarAudio();
    document.getElementById("estado").innerText = "🎧 Escuchando y analizando...";
}

function analizarAudio(){
    analyser.getFloatFrequencyData(data);
    const notasDetectadas = extraerNotas(data, ctx.sampleRate);
    if(notasDetectadas.length){
        const acorde = detectarAcorde(notasDetectadas);
        document.getElementById("estado").innerText = "🎵 Detectado: " + notasDetectadas.join(", ") + (acorde ? " | Acorde: " + acorde : "");
        // Iluminar piano
        notasDetectadas.forEach(n => {
            const el = document.getElementById("key-"+n+"4") || document.getElementById("key-"+n+"5");
            if(el) {
                el.classList.add("right-active");
                setTimeout(() => el.classList.remove("right-active"), 200);
            }
        });
    }
    requestAnimationFrame(analizarAudio);
}

/* ================= TU POLIFONÍA HEURÍSTICA ================= */
function extraerNotas(spec, sr){
    let notas = [];
    for(let i=5; i<300; i++){
        if(spec[i] > -45){
            let f = i * sr / 2048;
            let n = Math.round(12 * Math.log2(f/440) + 69);
            if(n > 20 && n < 100){
                let nota = NOTAS[n%12];
                if(!notas.includes(nota)) notas.push(nota);
            }
        }
    }
    return notas.slice(0, 4);
}

function detectarAcorde(n){
    const s = n.sort().join("");
    if(s.includes("CEG")) return "Do Mayor (C)";
    if(s.includes("DFA")) return "Re menor (Dm)";
    if(s.includes("FAC")) return "Fa Mayor (F)";
    return null;
}

/* ================= ÓRDENES Y CONTROL ================= */
function procesarOrden(){
    const t = document.getElementById("orden").value.toLowerCase();
    if(t.includes("rápido")) CEREBRO.estado.bpm += 10;
    if(t.includes("enseñar")) enseñar();
    document.getElementById("estado").innerText = "⚙ Acción: " + t + " | BPM: " + CEREBRO.estado.bpm;
}

function enseñar(){
    document.getElementById("estado").innerText = "👉 Sigue las luces para aprender...";
}

mediaFile.onchange = e => {
    document.getElementById("audioPlayer").src = URL.createObjectURL(e.target.files[0]);
};
</script>
</body>
</html>
"""

components.html(piano_html, height=850, scrolling=True)
