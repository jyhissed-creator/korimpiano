import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORIMPIANO&STUDY")

st.markdown("""
    <style>
    .stApp { background-color: #050008; }
    iframe { border-radius: 15px; border: 1px solid #333; }
    .footer { text-align: center; color: #6a00ff; padding: 10px; font-weight: bold; font-family: sans-serif; }
    </style>
""", unsafe_allow_html=True)

piano_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://unpkg.com/tone@14.8.49/build/Tone.js"></script>
    <style>
        body { background: #050008; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 10px; text-align: center; }
        .header { margin-bottom: 20px; border: 2px solid #6a00ff; border-radius: 15px; padding: 20px; background: rgba(106, 0, 255, 0.1); }
        h1 { margin: 0; color: #00ff88; letter-spacing: 2px; text-shadow: 0 0 10px #00ff8844; }
        .author { color: #aaa; font-size: 14px; margin-top: 5px; }
        
        .controls { display: flex; flex-direction: column; align-items: center; gap: 10px; }
        input { width: 80%; max-width: 600px; padding: 15px; background: #111; color: #00ff88; border: 1px solid #6a00ff; border-radius: 10px; font-size: 18px; outline: none; text-align: center; }
        button { width: 80%; max-width: 600px; padding: 15px; background: #6a00ff; color: white; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.3s; }
        button:hover { background: #00ff88; color: #000; box-shadow: 0 0 20px #00ff88; }
        
        #status { color: #00ff88; font-family: monospace; margin-top: 15px; min-height: 24px; font-size: 14px; }
        
        #piano-container { display: flex; justify-content: center; overflow-x: auto; padding: 30px 0; }
        #piano { display: flex; position: relative; height: 250px; }
        
        .key { position: relative; border: 1px solid #222; cursor: pointer; transition: 0.1s; user-select: none; }
        .white { width: 55px; height: 100%; background: linear-gradient(to bottom, #eee 0%, #fff 100%); border-radius: 0 0 5px 5px; z-index: 1; }
        .black { width: 36px; height: 150px; background: #222; margin-left: -18px; margin-right: -18px; z-index: 2; border-radius: 0 0 4px 4px; }
        
        .active { background: #00ff88 !important; box-shadow: 0 0 30px #00ff88 !important; transform: translateY(5px); }
        .active-bass { background: #ff00ff !important; box-shadow: 0 0 30px #ff00ff !important; transform: translateY(5px); }
        
        .label { position: absolute; bottom: 10px; width: 100%; text-align: center; font-size: 11px; font-weight: bold; color: #888; pointer-events: none; }
        .black .label { color: #555; bottom: 5px; }
    </style>
</head>
<body>

    <div class="header">
        <h1>🎹 KORIMPIANO & STUDY</h1>
        <p class="author">Creado por: <b>Yhissed Jiménez</b></p>
        <div class="controls">
            <input type="text" id="orden" placeholder="Ej: C/G, Am7, Dm, G7 o progresiones: C F G C">
            <button onclick="interpretar()">REPRODUCIR MÚSICA</button>
        </div>
        <div id="status">Esperando comando...</div>
    </div>

    <div id="piano-container">
        <div id="piano"></div>
    </div>

<script>
    const synth = new Tone.PolySynth(Tone.Synth).toDestination();
    const notesBase = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const keysData = [];

    // Generar 4 octavas para cubrir bajos y melodía (2 a 5)
    const piano = document.getElementById('piano');
    for (let oct = 2; oct <= 5; oct++) {
        notesBase.forEach(n => {
            const fullNote = n + oct;
            const isBlack = n.includes("#");
            const div = document.createElement('div');
            div.className = `key ${isBlack ? 'black' : 'white'}`;
            div.dataset.note = fullNote;
            div.dataset.simple = n;
            div.innerHTML = `<span class="label">${fullNote}</span>`;
            
            div.onmousedown = () => { playNote(fullNote); div.classList.add('active'); };
            div.onmouseup = () => div.classList.remove('active');
            
            piano.appendChild(div);
            keysData.push({ el: div, note: fullNote, simple: n, oct: oct });
        });
    }

    function playNote(n, isBass = false) {
        Tone.start();
        synth.triggerAttackRelease(n, "2n");
    }

    function highlightKey(noteName, octave, className) {
        const target = keysData.find(k => k.simple === noteName && k.oct === octave);
        if (target) {
            target.el.classList.add(className);
            setTimeout(() => target.el.classList.remove(className), 800);
        }
    }

    const chordsLib = {
        "M": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "maj7": [0, 4, 7, 11],
        "m7": [0, 3, 7, 10], "sus4": [0, 5, 7], "dim": [0, 3, 6], "aug": [0, 4, 8]
    };

    function parseChord(input) {
        // Limpieza y traducción de bemoles
        let str = input.toUpperCase().replace("BB", "A#").replace("EB", "D#").replace("AB", "G#").replace("DB", "C#").replace("GB", "F#");
        
        let bass = null;
        if (str.includes("/")) {
            [str, bass] = str.split("/");
        }

        let root = str[0];
        if (str[1] === "#") root = str.slice(0, 2);
        
        let typeRaw = str.replace(root, "").toLowerCase();
        let type = chordsLib[typeRaw] ? typeRaw : (typeRaw.includes("m") ? "m" : "M");
        
        return { root, type, bass };
    }

    async function interpretar() {
        const input = document.getElementById('orden').value.trim();
        const status = document.getElementById('status');
        if (!input) return;

        // Separar por espacios para permitir canciones/progresiones
        const items = input.split(/\s+/);
        
        for (let i = 0; i < items.length; i++) {
            const item = items[i];
            const { root, type, bass } = parseChord(item);
            const rootIdx = notesBase.indexOf(root);
            
            if (rootIdx !== -1) {
                status.innerText = `Tocando: ${item}`;
                let notesToPlay = [];

                // 1. Tocar el Bajo (Octava 2)
                if (bass) {
                    notesToPlay.push(bass + "2");
                    highlightKey(bass, 2, 'active-bass');
                } else {
                    notesToPlay.push(root + "2");
                    highlightKey(root, 2, 'active-bass');
                }

                // 2. Tocar el Acorde (Octava 4)
                chordsLib[type].forEach(interval => {
                    const nName = notesBase[(rootIdx + interval) % 12];
                    notesToPlay.push(nName + "4");
                    highlightKey(nName, 4, 'active');
                });

                synth.triggerAttackRelease(notesToPlay, "2n");
                
                // Si hay más acordes, esperar antes del siguiente
                if (items.length > 1) await new Promise(r => setTimeout(r, 1000));
            }
        }
        status.innerText = "Fin de la secuencia.";
    }
</script>
</body>
</html>
"""

components.html(piano_html, height=700, scrolling=False)

st.markdown('<div class="footer">KORIMPIANO&STUDY © 2026 | Una creación de Yhissed Jiménez</div>', unsafe_allow_html=True)
