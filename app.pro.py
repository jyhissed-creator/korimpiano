
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORIMPIANO&STUDY")

st.markdown("""
    <style>
    .stApp { background-color: #050008; }
    iframe { border-radius: 15px; border: 1px solid #333; }
    .footer { text-align: center; color: #6a00ff; padding: 15px; font-weight: bold; font-family: sans-serif; }
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
        body { background: #050008; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 10px; text-align: center; overflow-x: hidden; }
        .header { margin-bottom: 20px; border: 2px solid #6a00ff; border-radius: 15px; padding: 20px; background: rgba(106, 0, 255, 0.1); box-shadow: 0 0 15px rgba(106, 0, 255, 0.2); }
        h1 { margin: 0; color: #00ff88; letter-spacing: 2px; text-shadow: 0 0 10px #00ff8844; font-size: 22px; }
        .author { color: #aaa; font-size: 13px; margin-top: 5px; margin-bottom: 15px; }
        
        .controls { display: flex; flex-direction: column; align-items: center; gap: 12px; }
        input { width: 90%; max-width: 500px; padding: 15px; background: #111; color: #00ff88; border: 2px solid #6a00ff; border-radius: 10px; font-size: 18px; outline: none; text-align: center; }
        button { width: 90%; max-width: 500px; padding: 15px; background: #00ff88; color: #000; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; font-size: 16px; transition: 0.3s; }
        button:hover { background: #6a00ff; color: white; box-shadow: 0 0 20px #6a00ff; }
        
        #status { color: #00ff88; font-family: monospace; margin-top: 15px; min-height: 24px; font-size: 14px; text-transform: uppercase; }
        
        #piano-container { display: flex; justify-content: flex-start; overflow-x: auto; padding: 20px 5px; margin-top: 10px; -webkit-overflow-scrolling: touch; }
        #piano { display: flex; position: relative; height: 220px; margin: 0 auto; }
        
        .key { position: relative; border: 1px solid #111; cursor: pointer; transition: 0.1s; user-select: none; }
        .white { width: 45px; height: 100%; background: linear-gradient(to bottom, #eee 0%, #fff 100%); border-radius: 0 0 5px 5px; z-index: 1; }
        .black { width: 30px; height: 130px; background: #222; margin-left: -15px; margin-right: -15px; z-index: 2; border-radius: 0 0 4px 4px; }
        
        .active { background: #00ff88 !important; box-shadow: 0 0 25px #00ff88 !important; transform: translateY(4px); }
        .active-bass { background: #ff00ff !important; box-shadow: 0 0 25px #ff00ff !important; transform: translateY(4px); }
        
        .label { position: absolute; bottom: 8px; width: 100%; text-align: center; font-size: 10px; font-weight: bold; color: #999; pointer-events: none; }
        .black .label { color: #666; bottom: 5px; }
    </style>
</head>
<body>

    <div class="header">
        <h1>🎹 KORIMPIANO & STUDY</h1>
        <p class="author">Creado por: <b>Yhissed Jiménez</b></p>
        <div class="controls">
            <input type="text" id="orden" placeholder="C, Am, C/G, C-E-G o Am F C G">
            <button onclick="interpretar()">REPRODUCIR</button>
        </div>
        <div id="status">Listo para sonar</div>
    </div>

    <div id="piano-container">
        <div id="piano"></div>
    </div>

<script>
    const synth = new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: "triangle" },
        envelope: { attack: 0.05, release: 1 }
    }).toDestination();

    const notesBase = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const flatsMap = { "DB": "C#", "EB": "D#", "GB": "F#", "AB": "G#", "BB": "A#" };
    const keysData = [];

    // Generar piano de Octava 2 a 5
    const piano = document.getElementById('piano');
    for (let oct = 2; oct <= 5; oct++) {
        notesBase.forEach(n => {
            const fullNote = n + oct;
            const isBlack = n.includes("#");
            const div = document.createElement('div');
            div.className = `key ${isBlack ? 'black' : 'white'}`;
            div.dataset.note = fullNote;
            div.innerHTML = `<span class="label">${fullNote}</span>`;
            
            div.onmousedown = () => { playNote(fullNote); div.classList.add('active'); };
            div.onmouseup = () => div.classList.remove('active');
            piano.appendChild(div);
            keysData.push({ el: div, note: fullNote, simple: n, oct: oct });
        });
    }

    function playNote(note) {
        Tone.start();
        synth.triggerAttackRelease(note, "4n");
    }

    function highlight(simpleNote, oct, className) {
        const key = keysData.find(k => k.simple === simpleNote && k.oct === oct);
        if (key) {
            key.el.classList.add(className);
            setTimeout(() => key.el.classList.remove(className), 600);
        }
    }

    function normalizeNote(n) {
        let note = n.toUpperCase().trim();
        for (let flat in flatsMap) { note = note.replace(flat, flatsMap[flat]); }
        return note;
    }

    async function interpretar() {
        const rawInput = document.getElementById('orden').value.trim();
        const status = document.getElementById('status');
        if (!rawInput) return;

        // Separar por espacios si es una progresión (Ej: C Am F G)
        const parts = rawInput.split(/\s+/);
        
        for (let item of parts) {
            let notesToPlay = [];
            status.innerText = "Interpretando: " + item;

            // CASO 1: Notas individuales con guion (Ej: C-E-G)
            if (item.includes("-")) {
                const notes = item.split("-");
                notes.forEach(n => {
                    const norm = normalizeNote(n);
                    notesToPlay.push(norm + "4");
                    highlight(norm, 4, 'active');
                });
            } 
            // CASO 2: Acordes con Bajos (Ej: C/G)
            else if (item.includes("/")) {
                const [chord, bass] = item.split("/");
                const normBass = normalizeNote(bass);
                notesToPlay.push(normBass + "2");
                highlight(normBass, 2, 'active-bass');
                
                // Extraer raíz del acorde
                let root = normalizeNote(chord);
                if (root.endsWith("M") || root.endsWith("m")) root = root.slice(0, -1);
                
                notesToPlay.push(root + "4");
                highlight(root, 4, 'active');
            }
            // CASO 3: Acorde o Nota simple (Ej: Am o C)
            else {
                const norm = normalizeNote(item);
                // Si es acorde menor (termina en M o m)
                let root = norm;
                if (norm.length > 1 && (norm.endsWith("M") || norm.endsWith("m"))) {
                    root = norm.slice(0, -1);
                }
                
                // Para simplificar, si es acorde solo tocamos Triada Básica
                notesToPlay.push(root + "4");
                highlight(root, 4, 'active');
                
                // Añadir tercera y quinta automáticamente si parece acorde
                const rootIdx = notesBase.indexOf(root);
                if (rootIdx !== -1) {
                   const isMinor = norm.includes("M"); 
                   const thirdIdx = (rootIdx + (isMinor ? 3 : 4)) % 12;
                   const fifthIdx = (rootIdx + 7) % 12;
                   notesToPlay.push(notesBase[thirdIdx] + "4");
                   notesToPlay.push(notesBase[fifthIdx] + "4");
                   highlight(notesBase[thirdIdx], 4, 'active');
                   highlight(notesBase[fifthIdx], 4, 'active');
                }
            }

            if (notesToPlay.length > 0) {
                synth.triggerAttackRelease(notesToPlay, "2n");
            }
            
            if (parts.length > 1) await new Promise(r => setTimeout(r, 1200));
        }
        status.innerText = "Fin de la secuencia.";
    }
</script>
</body>
</html>
"""

components.html(piano_html, height=650, scrolling=False)

st.markdown('<div class="footer">KORIMPIANO&STUDY © 2026 | Una creación de Yhissed Jiménez</div>', unsafe_allow_html=True)
