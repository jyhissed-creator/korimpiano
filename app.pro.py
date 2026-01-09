import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORIMPIANO&STUDY")

# Estilo Global
st.markdown("""
    <style>
    .stApp { background-color: #050008; }
    iframe { border-radius: 15px; }
    .footer { text-align: center; color: #6a00ff; padding: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

piano_ia_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://unpkg.com/tone@14.8.49/build/Tone.js"></script>
    <style>
        body { background: #050008; color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 10px; text-align: center; }
        .header { margin-bottom: 20px; border: 2px solid #6a00ff; border-radius: 15px; padding: 20px; background: rgba(106, 0, 255, 0.05); }
        h1 { margin: 0; color: #00ff88; letter-spacing: 2px; font-size: 24px; }
        p.author { color: #888; font-size: 14px; margin-top: 5px; }
        
        input { width: 70%; padding: 12px; background: #111; color: #00ff88; border: 1px solid #6a00ff; border-radius: 8px; font-size: 18px; margin-bottom: 10px; outline: none; }
        button { width: 70%; padding: 12px; background: #6a00ff; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.3s; }
        button:hover { background: #00ff88; color: #000; }
        
        #status { color: #00ff88; font-family: monospace; margin-top: 15px; height: 20px; }
        
        #piano-container { display: flex; justify-content: center; overflow-x: auto; padding: 20px 0; margin-top: 20px; }
        #piano { display: flex; position: relative; height: 220px; }
        
        .key { position: relative; border: 1px solid #222; cursor: pointer; transition: background 0.1s, transform 0.1s; }
        .white { width: 50px; height: 100%; background: white; border-radius: 0 0 5px 5px; z-index: 1; color: #333; }
        .black { width: 34px; height: 130px; background: #222; margin-left: -17px; margin-right: -17px; z-index: 2; border-radius: 0 0 3px 3px; border: 1px solid #000; }
        
        .active { background: #00ff88 !important; box-shadow: 0 0 30px #00ff88 !important; transform: translateY(4px); }
        .label { position: absolute; bottom: 10px; width: 100%; text-align: center; font-size: 12px; pointer-events: none; font-weight: bold; }
        .black .label { color: #fff; bottom: 5px; font-size: 10px; }
    </style>
</head>
<body>

    <div class="header">
        <h1>🎹 KORIMPIANO & STUDY</h1>
        <p class="author">Creado por: <b>Yhissed Jiménez</b></p>
        <input type="text" id="orden" placeholder="Ej: C, Am, F#, Bb, G-B-D...">
        <br>
        <button onclick="comandar()">EJECUTAR COMANDO</button>
        <div id="status">Presiona una tecla o escribe un acorde</div>
    </div>

    <div id="piano-container">
        <div id="piano"></div>
    </div>

<script>
    // Configuración del sintetizador
    const synth = new Tone.PolySynth(Tone.Synth).toDestination();
    const notesBase = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const keysData = [];

    // Mapeo de Bemoles a Sostenidos
    const flatsToSharps = { "DB": "C#", "EB": "D#", "GB": "F#", "AB": "G#", "BB": "A#" };

    // Generar Piano (Octavas 3 y 4)
    const piano = document.getElementById('piano');
    for (let oct = 3; oct <= 4; oct++) {
        notesBase.forEach(n => {
            const fullNote = n + oct;
            const isBlack = n.includes("#");
            const div = document.createElement('div');
            div.className = `key ${isBlack ? 'black' : 'white'}`;
            div.dataset.note = fullNote;
            div.dataset.simple = n;
            div.innerHTML = `<span class="label">${fullNote}</span>`;
            
            div.addEventListener('mousedown', () => { 
                playNote(fullNote); 
                div.classList.add('active'); 
            });
            div.addEventListener('mouseup', () => div.classList.remove('active'));
            div.addEventListener('mouseleave', () => div.classList.remove('active'));
            
            piano.appendChild(div);
            keysData.push({ el: div, note: fullNote, simple: n });
        });
    }

    async function playNote(n) {
        if (Tone.context.state !== 'running') await Tone.start();
        synth.triggerAttackRelease(n, "2n");
    }

    function comandar() {
        let rawInput = document.getElementById('orden').value.toUpperCase().trim();
        const status = document.getElementById('status');
        keysData.forEach(k => k.el.classList.remove('active'));

        if (!rawInput) return;

        // 1. Reemplazar Bemoles por Sostenidos (Ej: Bb -> A#)
        for (let flat in flatsToSharps) {
            rawInput = rawInput.replace(flat, flatsToSharps[flat]);
        }

        // 2. Lógica de Secuencia manual (C-E-G)
        if (rawInput.includes("-")) {
            const parts = rawInput.split("-");
            parts.forEach(p => {
                let found = keysData.find(k => k.simple === p || k.note === p);
                if (found) { found.el.classList.add('active'); playNote(found.note); }
            });
            status.innerText = "Tocando secuencia: " + rawInput;
            return;
        }

        // 3. Lógica de Acordes Completa
        const chordTypes = {
            "M": [0, 4, 7],      // Mayor
            "MIN": [0, 3, 7],    // Menor
            "M7": [0, 4, 7, 10]  // Séptima
        };

        let root = "";
        let type = "M";

        // Detectar si la raíz es sostenida (C#) o simple (C)
        if (rawInput.length >= 2 && rawInput[1] === "#") {
            root = rawInput.slice(0, 2);
            type = rawInput.slice(2) || "M";
        } else {
            root = rawInput[0];
            type = rawInput.slice(1) || "M";
        }

        // Normalizar nombres de tipos
        if (type === "m") type = "MIN";
        if (type === "MINOR") type = "MIN";

        let rootIdx = notesBase.indexOf(root);

        if (rootIdx !== -1) {
            let intervals = chordTypes[type] || chordTypes["M"];
            intervals.forEach(interval => {
                let noteIdx = (rootIdx + interval) % 12;
                let noteName = notesBase[noteIdx];
                // Intentar tocar en la octava 4
                let target = keysData.find(k => k.note === noteName + "4");
                if (target) { target.el.classList.add('active'); playNote(target.note); }
            });
            status.innerText = `Tocando Acorde: ${root} ${type}`;
        } else {
            status.innerText = "Error: Comando no reconocido";
        }
    }
</script>
</body>
</html>
"""

components.html(piano_ia_html, height=650, scrolling=False)

st.markdown('<div class="footer">KORIMPIANO&STUDY © 2024 - Powered by Yhissed Jiménez</div>', unsafe_allow_html=True)
