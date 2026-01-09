import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORYM.PIANO Studio")

st.markdown("""
    <style>
    .stApp { background-color: #050008; }
    footer {visibility: hidden;}
    iframe { border-radius: 20px; box-shadow: 0 0 35px #00ff8833; border: 1px solid #1a1a1a; }
    </style>
""", unsafe_allow_html=True)

piano_studio_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://unpkg.com/tone@14.8.49/build/Tone.js"></script>
    <style>
        body { background: #050008; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 15px; text-align: center; }
        .creator-brand { font-size: 11px; color: #6a00ff; letter-spacing: 4px; font-weight: bold; margin-bottom: 10px; }
        .system-title { font-size: 26px; font-weight: 800; color: #fff; margin: 0 0 20px 0; }
        
        .main-panel { background: #000; border: 1px solid #00ff88; border-radius: 15px; padding: 20px; max-width: 800px; margin: 0 auto; }
        textarea { width: 95%; height: 120px; background: #0a0a0a; color: #00ff88; border: 1px solid #333; border-radius: 8px; padding: 10px; font-size: 14px; margin-bottom: 15px; resize: none; outline: none; font-family: monospace; }
        
        .controls { display: flex; gap: 10px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
        .btn-audio { background: #00ff88; color: black; border: 2px solid #00ff88; }
        .btn-play { background: #6a00ff; color: white; }
        
        button { padding: 12px 20px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; text-transform: uppercase; }
        button:hover { opacity: 0.8; transform: translateY(-2px); }
        
        #piano-container { display: flex; justify-content: center; overflow-x: auto; padding: 25px 0; }
        #piano { display: flex; position: relative; height: 180px; }
        
        .key { position: relative; border: 1px solid #222; cursor: pointer; transition: 0.1s; }
        .white { width: 40px; height: 100%; background: #fff; border-radius: 0 0 5px 5px; z-index: 1; }
        .black { width: 26px; height: 110px; background: #222; margin-left: -13px; margin-right: -13px; z-index: 2; border-radius: 0 0 3px 3px; }
        .active { background: #00ff88 !important; box-shadow: 0 0 25px #00ff88 !important; }
        
        #status { color: #00ff88; font-family: monospace; font-size: 13px; margin-top: 10px; border-top: 1px solid #222; padding-top: 10px; }
    </style>
</head>
<body>

    <div class="creator-brand">YHISSED JIMÉNEZ PRESENTA</div>
    <div class="system-title">KORYM.PIANO STUDIO</div>

    <div class="main-panel">
        <button class="btn-audio" onclick="activarAudio()">1. ACTIVAR AUDIO</button>
        <p style="font-size: 10px; color: #666;">(Presiona antes de empezar)</p>
        
        <textarea id="song-input" placeholder="Pega letra con acordes. Ejemplo: (C) Hola (G) mundo (Am) musical"></textarea>
        
        <div class="controls">
            <button class="btn-play" onclick="interpretarCancion()">2. REPRODUCIR</button>
            <button onclick="detener()" style="background:#444;">DETENER</button>
        </div>
        <div id="status">ESTADO: ESPERANDO ACTIVACIÓN</div>
    </div>

    <div id="piano-container"><div id="piano"></div></div>

<script>
    // Configuración del Sintetizador
    const synth = new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: "amsine" },
        envelope: { attack: 0.1, decay: 0.2, sustain: 0.5, release: 0.8 }
    }).toDestination();

    const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const chordsMap = { "M": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "MAJ7": [0, 4, 7, 11] };
    const keysData = [];

    // Construcción del Piano
    const piano = document.getElementById('piano');
    for (let oct = 3; oct <= 5; oct++) {
        notes.forEach(n => {
            const fullNote = n + oct;
            const div = document.createElement('div');
            div.className = `key ${n.includes("#") ? 'black' : 'white'}`;
            div.onmousedown = () => { playNote(fullNote); div.classList.add('active'); };
            div.onmouseup = () => div.classList.remove('active');
            piano.appendChild(div);
            keysData.push({ el: div, note: fullNote, simple: n });
        });
    }

    async function activarAudio() {
        await Tone.start();
        document.getElementById('status').innerText = "AUDIO ACTIVADO: KORYM.PIANO LISTO";
        document.querySelector('.btn-audio').style.background = "#444";
        document.querySelector('.btn-audio').innerText = "AUDIO ONLINE";
    }

    function playNote(n, time = 0) {
        synth.triggerAttackRelease(n, "2n", Tone.now() + time);
        const key = keysData.find(k => k.note === n);
        if(key) {
            setTimeout(() => key.el.classList.add('active'), time * 1000);
            setTimeout(() => key.el.classList.remove('active'), (time * 1000) + 600);
        }
    }

    function detener() {
        Tone.Transport.stop();
        keysData.forEach(k => k.el.classList.remove('active'));
    }

    function interpretarCancion() {
        if (Tone.context.state !== 'running') {
            alert("Por favor, presiona el botón 'ACTIVAR AUDIO' primero.");
            return;
        }

        const text = document.getElementById('song-input').value.toUpperCase();
        const words = text.match(/\\((.*?)\\)|([A-G][#B]?[M7]?)/g) || [];
        let time = 0;

        words.forEach(word => {
            let clean = word.replace(/[()\\s]/g, "");
            let root = "";
            let type = "M";

            // Lógica de detección de acordes
            if (notes.includes(clean[0])) {
                if (clean[1] === "#" || clean[1] === "B") {
                    root = clean.substring(0, 2).replace("BB", "A#");
                    type = clean.substring(2) || "M";
                } else {
                    root = clean[0];
                    type = clean.substring(1) || "M";
                }

                let rootIdx = notes.indexOf(root);
                if (rootIdx !== -1) {
                    let intervals = chordsMap[type] || chordsMap["M"];
                    intervals.forEach(inter => {
                        let noteName = notes[(rootIdx + inter) % 12];
                        playNote(noteName + "4", time);
                    });
                    time += 1.5; // Tiempo entre acordes
                }
            }
        });
        document.getElementById('status').innerText = "KORYM.PIANO: TOCANDO TU CANCIÓN...";
    }
</script>
</body>
</html>
"""

components.html(piano_studio_html, height=850, scrolling=False)
