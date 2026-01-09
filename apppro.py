import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORYM AI Piano Virtual")

# Estilo para arreglar la interfaz en móviles
st.markdown("""
    <style>
    .stApp { background-color: #050008; }
    iframe { border-radius: 15px; box-shadow: 0 0 20px #6a00ff44; }
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
        body { background: #050008; color: white; font-family: sans-serif; margin: 0; padding: 10px; text-align: center; }
        .console { background: #000; border: 2px solid #00ff88; border-radius: 15px; padding: 15px; margin-bottom: 15px; }
        input { width: 80%; padding: 12px; background: #111; color: #00ff88; border: 1px solid #333; border-radius: 8px; font-size: 18px; margin-bottom: 10px; }
        button { width: 80%; padding: 12px; background: #6a00ff; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; }
        
        #piano-container { display: flex; justify-content: center; overflow-x: auto; padding-bottom: 20px; background: #000; border-radius: 10px; }
        #piano { display: flex; position: relative; height: 200px; padding: 10px; }
        
        .key { position: relative; border: 1px solid #222; cursor: pointer; transition: 0.1s; }
        .white { width: 45px; height: 100%; background: white; border-radius: 0 0 5px 5px; z-index: 1; }
        .black { width: 30px; height: 120px; background: #222; margin-left: -15px; margin-right: -15px; z-index: 2; border-radius: 0 0 3px 3px; }
        
        .active { background: #00ff88 !important; box-shadow: 0 0 30px #00ff88 !important; transform: translateY(5px); }
        .label { position: absolute; bottom: 5px; width: 100%; text-align: center; color: #888; font-size: 10px; pointer-events: none; font-weight: bold; }
    </style>
</head>
<body>

    <div class="console">
        <h3 style="margin:0 0 10px 0;">🎹 KORYM AI: REPARADO</h3>
        <input type="text" id="orden" placeholder="Escribe: C, Bb, Am, C-E-G...">
        <button onclick="comandar()">EJECUTAR COMANDO</button>
        <div id="status" style="color:#00ff88; font-family:monospace; margin-top:10px; font-size:14px;">Listo para recibir órdenes exactas.</div>
    </div>

    <div id="piano-container">
        <div id="piano"></div>
    </div>

<script>
    const synth = new Tone.PolySynth(Tone.Synth).toDestination();
    const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const keysData = [];

    // Generar 3 octavas exactas (Octavas 3, 4 y 5)
    const piano = document.getElementById('piano');
    for (let oct = 3; oct <= 5; oct++) {
        notes.forEach(n => {
            const fullNote = n + oct;
            const isBlack = n.includes("#");
            const div = document.createElement('div');
            div.className = `key ${isBlack ? 'black' : 'white'}`;
            div.dataset.note = fullNote;
            div.dataset.simple = n;
            div.innerHTML = `<span class="label">${fullNote}</span>`;
            
            div.onmousedown = () => { play(fullNote); div.classList.add('active'); };
            div.onmouseup = () => div.classList.remove('active');
            
            piano.appendChild(div);
            keysData.push({ el: div, note: fullNote, simple: n });
        });
    }

    function play(n) {
        Tone.start();
        synth.triggerAttackRelease(n, "4n");
    }

    function comandar() {
        const input = document.getElementById('orden').value.toUpperCase().trim();
        const status = document.getElementById('status');
        keysData.forEach(k => k.el.classList.remove('active'));

        // 1. Diccionario de Acordes
        const chords = {
            "M": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "MAJ7": [0, 4, 7, 11]
        };

        // Normalizar Bb a A# para el sistema
        let search = input.replace("BB", "A#").replace("EB", "D#").replace("AB", "G#").replace("DB", "C#").replace("GB", "F#");

        // Lógica de Notas separadas por guion (C-E-G)
        if (search.includes("-")) {
            const parts = search.split("-");
            parts.forEach(p => {
                let found = keysData.filter(k => k.simple === p || k.note === p);
                found.forEach(f => { f.el.classList.add('active'); play(f.note); });
            });
            status.innerText = "Tocando secuencia exacta.";
            return;
        }

        // Lógica de Acordes (Am, C, F#m)
        let root = search[0];
        if (search[1] === "#") root = search.slice(0, 2);
        let type = search.replace(root, "") || "M";
        
        let rootIdx = notes.indexOf(root);
        if (rootIdx !== -1) {
            let intervals = chords[type] || chords["M"];
            intervals.forEach(interval => {
                let noteName = notes[(rootIdx + interval) % 12];
                // Iluminar en la octava 4 (central)
                let target = keysData.find(k => k.note === noteName + "4");
                if (target) { target.el.classList.add('active'); play(target.note); }
            });
            status.innerText = `Acorde de ${root} ${type} ejecutado correctamente.`;
        } else {
            // Nota simple
            let found = keysData.filter(k => k.simple === search || k.note === search);
            if (found.length > 0) {
                found.forEach(f => { f.el.classList.add('active'); play(f.note); });
                status.innerText = `Nota ${search} activada.`;
            } else {
                status.innerText = "Error: Nota o Acorde no reconocido.";
            }
        }
    }
</script>
</body>
</html>
"""

components.html(piano_ia_html, height=700, scrolling=False)
