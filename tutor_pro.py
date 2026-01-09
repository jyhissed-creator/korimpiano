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
        textarea { width: 95%; height: 100px; background: #0a0a0a; color: #00ff88; border: 1px solid #333; border-radius: 8px; padding: 10px; font-size: 14px; margin-bottom: 10px; resize: none; outline: none; }
        .controls { display: flex; gap: 10px; justify-content: center; margin-bottom: 10px; flex-wrap: wrap; }
        
        input[type="number"] { width: 60px; background: #111; border: 1px solid #6a00ff; color: white; padding: 8px; border-radius: 5px; }
        button { padding: 12px 25px; background: #6a00ff; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        button:hover { background: #00ff88; color: #000; }
        
        #piano-container { display: flex; justify-content: center; overflow-x: auto; padding: 25px 0; }
        #piano { display: flex; position: relative; height: 200px; }
        
        .key { position: relative; border: 1px solid #222; cursor: pointer; transition: 0.1s; }
        .white { width: 42px; height: 100%; background: #fff; border-radius: 0 0 5px 5px; z-index: 1; }
        .black { width: 28px; height: 120px; background: #222; margin-left: -14px; margin-right: -14px; z-index: 2; border-radius: 0 0 3px 3px; }
        .active { background: #00ff88 !important; box-shadow: 0 0 30px #00ff88 !important; transform: translateY(5px); }
        .label { position: absolute; bottom: 8px; width: 100%; text-align: center; color: #999; font-size: 9px; font-weight: bold; }
    </style>
</head>
<body>

    <div class="creator-brand">YHISSED JIMÉNEZ PRESENTA</div>
    <div class="system-title">KORYM.PIANO STUDIO</div>

    <div class="main-panel">
        <textarea id="song-input" placeholder="Pega aquí la letra con acordes o una secuencia (ej: C Am F G)"></textarea>
        <div class="controls">
            <div>
                <label style="font-size:12px;">VELOCIDAD (BPM):</label>
                <input type="number" id="bpm" value="120" min="40" max="220">
            </div>
            <button onclick="interpretarCancion()">REPRODUCIR MÚSICA</button>
            <button onclick="detener()" style="background:#cc0000;">PARAR</button>
        </div>
        <div id="status" style="color:#00ff88; font-family:monospace; font-size:12px;">REGISTRO: KORYM.PIANO LISTO</div>
    </div>

    <div id="piano-container"><div id="piano"></div></div>

<script>
    const synth = new Tone.PolySynth(Tone.Synth).toDestination();
    const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const chordsMap = { "M": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "MAJ7": [0, 4, 7, 11] };
    const keysData = [];

    // Generar Piano
    const piano = document.getElementById('piano');
    for (let oct = 3; oct <= 5; oct++) {
        notes.forEach(n => {
            const fullNote = n + oct;
            const div = document.createElement('div');
            div.className = `key ${n.includes("#") ? 'black' : 'white'}`;
            div.innerHTML = `<span class="label">${fullNote}</span>`;
            div.onmousedown = () => { playNote(fullNote); div.classList.add('active'); };
            div.onmouseup = () => div.classList.remove('active');
            piano.appendChild(div);
            keysData.push({ el: div, note: fullNote, simple: n });
        });
    }

    function playNote(n, time = 0, duration = "4n") {
        synth.triggerAttackRelease(n, duration, time);
        const key = keysData.find(k => k.note === n);
        if(key) {
            setTimeout(() => key.el.classList.add('active'), time * 1000);
            setTimeout(() => key.el.classList.remove('active'), (time * 1000) + 400);
        }
    }

    function detener() { Tone.Transport.stop(); Tone.Transport.cancel(); }

    async function interpretarCancion() {
        await Tone.start();
        detener();
        
        const text = document.getElementById('song-input').value.toUpperCase();
        const bpm = document.getElementById('bpm').value;
        Tone.Transport.bpm.value = bpm;

        // Extraer solo lo que parezca acordes (C, Am, F#, etc.)
        const words = text.split(/[\\s\\n]+/);
        let time = 0;

        words.forEach(word => {
            // Limpiar símbolos comunes en letras de canciones
            let clean = word.replace(/[()[\\]]/g, "");
            let root = "";
            let type = "M";

            if (notes.includes(clean[0])) {
                if (clean[1] === "#" || clean[1] === "B") {
                    root = clean.substring(0, 2).replace("BB", "A#");
                    type = clean.substring(2) || "M";
                } else {
                    root = clean[0];
                    type = clean.substring(1) || "M";
                }
                if (type === "MIN" || type === "M") type = "m"; // Ajuste menor común

                let rootIdx = notes.indexOf(root);
                if (rootIdx !== -1) {
                    let intervals = chordsMap[type] || chordsMap["M"];
                    intervals.forEach(inter => {
                        let noteName = notes[(rootIdx + inter) % 12];
                        playNote(noteName + "4", time);
                    });
                    time += (60 / bpm) * 2; // Espacio entre acordes según ritmo
                }
            }
        });
        
        document.getElementById('status').innerText = "KORYM.PIANO: Interpretando canción de Yhissed...";
    }
</script>
</body>
</html>
"""

components.html(piano_studio_html, height=800, scrolling=False)
