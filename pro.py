import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORYM AI Piano Virtual")

# Estilo para arreglar la interfaz en móviles
st.markdown("""
    <style>
    .stApp { background-color: #050008; }
    iframe { border-radius: 15px; box-shadow: 0 0 25px #6a00ff66; border: 1px solid #333; }
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
        .creator { font-size: 12px; color: #6a00ff; letter-spacing: 2px; margin-bottom: 5px; font-weight: bold; }
        .console { background: #000; border: 2px solid #00ff88; border-radius: 15px; padding: 15px; margin-bottom: 15px; box-shadow: inset 0 0 10px #00ff8822; }
        input { width: 85%; padding: 12px; background: #111; color: #00ff88; border: 1px solid #333; border-radius: 8px; font-size: 18px; margin-bottom: 10px; outline: none; }
        input:focus { border-color: #00ff88; }
        button { width: 85%; padding: 12px; background: #6a00ff; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 16px; text-transform: uppercase; }
        
        #piano-container { display: flex; justify-content: center; overflow-x: auto; padding-bottom: 20px; background: #000; border-radius: 10px; }
        #piano { display: flex; position: relative; height: 220px; padding: 10px; }
        
        .key { position: relative; border: 1px solid #222; cursor: pointer; transition: 0.1s; }
        .white { width: 45px; height: 100%; background: linear-gradient(to bottom, #eee 0%, #fff 100%); border-radius: 0 0 5px 5px; z-index: 1; }
        .black { width: 30px; height: 130px; background: linear-gradient(to bottom, #444 0%, #000 100%); margin-left: -15px; margin-right: -15px; z-index: 2; border-radius: 0 0 3px 3px; }
        
        .active { background: #00ff88 !important; box-shadow: 0 0 30px #00ff88 !important; transform: translateY(4px); }
        .label { position: absolute; bottom: 8px; width: 100%; text-align: center; color: #888; font-size: 11px; pointer-events: none; font-weight: bold; }
    </style>
</head>
<body>

    <div class="creator">CREADO POR YHISSED JIMÉNEZ</div>
    <div class="console">
        <h2 style="margin:0 0 10px 0; color: #fff; letter-spacing: 1px;">🎹 KORYM.PIANO AI</h2>
        <input type="text" id="orden" placeholder="Escribe: C, Bb, Am, C-E-G...">
        <button onclick="comandar()">PROCESAR COMANDO</button>
        <div id="status" style="color:#00ff88; font-family: 'Courier New', monospace; margin-top:10px; font-size:13px;">Iniciando sistema...</div>
    </div>

    <div id="piano-container">
        <div id="piano"></div>
    </div>

<script>
    const synth = new Tone.PolySynth(Tone.Synth).toDestination();
    const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const keysData = [];

    // Registro del Sistema al cargar
    window.onload = () => {
        setTimeout(() => {
            document.getElementById('status').innerText = "REGISTRADO COMO: KORYM.PIANO [ACTIVE]";
        }, 1000);
    }

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

        const chords = {
            "M": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "MAJ7": [0, 4, 7, 11]
        };

        let search = input.replace("BB", "A#").replace("EB", "D#").replace("AB", "G#").replace("DB", "C#").replace("GB", "F#");

        if (search.includes("-")) {
            const parts = search.split("-");
            parts.forEach(p => {
                let found = keysData.filter(k => k.simple === p || k.note === p);
                found.forEach(f => { f.el.classList.add('active'); play(f.note); });
            });
            status.innerText = "KORYM.PIANO: Ejecutando secuencia manual.";
            return;
        }

        let root = search[0];
        if (search[1] === "#") root = search.slice(0, 2);
        let type = search.replace(root, "") || "M";
        
        let rootIdx = notes.indexOf(root);
        if (rootIdx !== -1) {
            let intervals = chords[type] || chords["M"];
            intervals.forEach(interval => {
                let noteName = notes[(rootIdx + interval) % 12];
                let target = keysData.find(k => k.note === noteName + "4");
                if (target) { target.el.classList.add('active'); play(target.note); }
            });
            status.innerText = `KORYM.PIANO: Acorde ${root}${type} ejecutado.`;
        } else {
            let found = keysData.filter(k => k.simple === search || k.note === search);
            if (found.length > 0) {
                found.forEach(f => { f.el.classList.add('active'); play(f.note); });
                status.innerText = `KORYM.PIANO: Nota ${search} activa.`;
            } else {
                status.innerText = "KORYM.PIANO: Error en comando.";
            }
        }
    }
</script>
</body>
</html>
"""

components.html(piano_ia_html, height=720, scrolling=False)
