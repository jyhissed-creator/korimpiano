import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORIMPIANO&STUDY")

st.markdown("""
    <style>
    .stApp { background-color: #050008; }
    iframe { border-radius: 20px; border: 2px solid #6a00ff; }
    .footer { text-align: center; color: #6a00ff; padding: 20px; font-weight: bold; font-family: sans-serif; }
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
        h1 { margin: 0; color: #00ff88; letter-spacing: 2px; text-transform: uppercase; font-size: 20px; }
        .author { color: #888; font-size: 12px; margin-top: 5px; }
        
        .ui-container { display: flex; flex-direction: column; align-items: center; gap: 10px; margin-top: 15px; }
        input { width: 90%; max-width: 450px; padding: 15px; background: #000; color: #00ff88; border: 2px solid #6a00ff; border-radius: 10px; font-size: 18px; text-align: center; outline: none; }
        button { width: 90%; max-width: 450px; padding: 15px; background: #00ff88; color: #000; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; font-size: 16px; text-transform: uppercase; }
        
        #status { color: #00ff88; font-family: monospace; margin-top: 10px; font-size: 14px; min-height: 20px; }
        
        #piano-scroll { display: flex; justify-content: flex-start; overflow-x: auto; padding: 20px 0; margin-top: 10px; border-top: 1px solid #333; }
        #piano { display: flex; position: relative; height: 200px; margin: 0 auto; }
        
        .key { position: relative; border: 1px solid #111; cursor: pointer; user-select: none; }
        .white { width: 42px; height: 100%; background: white; border-radius: 0 0 5px 5px; z-index: 1; }
        .black { width: 28px; height: 120px; background: #222; margin-left: -14px; margin-right: -14px; z-index: 2; border-radius: 0 0 3px 3px; }
        
        .active { background: #00ff88 !important; box-shadow: 0 0 20px #00ff88; z-index: 3; }
        .active-bass { background: #ff00ff !important; box-shadow: 0 0 20px #ff00ff; z-index: 3; }
        
        .label { position: absolute; bottom: 5px; width: 100%; text-align: center; font-size: 9px; font-weight: bold; color: #aaa; pointer-events: none; }
    </style>
</head>
<body>

    <div class="header">
        <h1>🎹 KORIMPIANO & STUDY</h1>
        <p class="author">Creado por: <b>Yhissed Jiménez</b></p>
        <div class="ui-container">
            <input type="text" id="input" placeholder="Ej: C-E-G (melodía) o C/G (acorde/bajo) o Am F C G">
            <button onclick="ejecutar()">REPRODUCIR</button>
        </div>
        <div id="status">Listo</div>
    </div>

    <div id="piano-scroll">
        <div id="piano"></div>
    </div>

<script>
    const synth = new Tone.PolySynth(Tone.Sampler).toDestination();
    const notesBase = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const pianoKeys = [];

    // Dibujar Piano (Octavas 2 a 5)
    const pianoDiv = document.getElementById('piano');
    for (let oct = 2; oct <= 5; oct++) {
        notesBase.forEach(n => {
            const isBlack = n.includes("#");
            const key = document.createElement('div');
            key.className = `key ${isBlack ? 'black' : 'white'}`;
            key.dataset.note = n + oct;
            key.innerHTML = `<span class="label">${n}${oct}</span>`;
            key.onmousedown = () => { play(n+oct); key.classList.add('active'); };
            key.onmouseup = () => key.classList.remove('active');
            pianoDiv.appendChild(key);
            pianoKeys.push({ el: key, note: n, oct: oct });
        });
    }

    function play(note) {
        Tone.start();
        synth.triggerAttackRelease(note, "2n");
    }

    function highlight(note, oct, type) {
        const k = pianoKeys.find(x => x.note === note && x.oct === oct);
        if (k) {
            const cls = type === 'bass' ? 'active-bass' : 'active';
            k.el.classList.add(cls);
            setTimeout(() => k.el.classList.remove(cls), 800);
        }
    }

    const chordsLib = {
        "m": [0, 3, 7], "": [0, 4, 7], "7": [0, 4, 7, 10], "maj7": [0, 4, 7, 11]
    };

    function fixNote(n) {
        return n.toUpperCase().replace("BB", "A#").replace("EB", "D#").replace("AB", "G#").replace("DB", "C#").replace("GB", "F#").trim();
    }

    async function ejecutar() {
        const val = document.getElementById('input').value.trim();
        const status = document.getElementById('status');
        if (!val) return;

        // Limpiar el estado anterior
        const segments = val.split(/\s+/); // Separar por espacios (progresiones)

        for (let seg of segments) {
            status.innerText = "Tocando: " + seg;
            let toPlay = [];

            // 1. MELODÍA (Notas con guion C-E-G)
            if (seg.includes("-")) {
                const notes = seg.split("-");
                notes.forEach(n => {
                    let fn = fixNote(n);
                    toPlay.push(fn + "4");
                    highlight(fn, 4, 'note');
                });
            }
            // 2. ACORDE CON BAJO (C/G)
            else if (seg.includes("/")) {
                const [chord, bass] = seg.split("/");
                const fb = fixNote(bass);
                const fc = fixNote(chord);
                
                // Bajo en octava grave
                toPlay.push(fb + "2");
                highlight(fb, 2, 'bass');

                // Acorde en octava media
                let root = fc.replace(/M|m|7/g, "");
                let type = fc.includes("m") ? "m" : "";
                let rootIdx = notesBase.indexOf(root);
                chordsLib[type].forEach(interval => {
                    let n = notesBase[(rootIdx + interval) % 12];
                    toPlay.push(n + "4");
                    highlight(n, 4, 'note');
                });
            }
            // 3. ACORDE O NOTA SIMPLE
            else {
                let fn = fixNote(seg);
                let root = fn.replace(/M|m|7/g, "");
                let type = fn.includes("m") ? "m" : (notesBase.includes(fn) ? null : "");
                
                if (type === null) { // Es nota sola
                    toPlay.push(fn + "4");
                    highlight(fn, 4, 'note');
                } else { // Es acorde
                    let rootIdx = notesBase.indexOf(root);
                    chordsLib[type].forEach(interval => {
                        let n = notesBase[(rootIdx + interval) % 12];
                        toPlay.push(n + "4");
                        highlight(n, 4, 'note');
                    });
                }
            }

            if (toPlay.length > 0) synth.triggerAttackRelease(toPlay, "2n");
            if (segments.length > 1) await new Promise(r => setTimeout(r, 1200));
        }
        status.innerText = "Fin.";
    }
</script>
</body>
</html>
"""

components.html(piano_html, height=650, scrolling=False)

st.markdown('<div class="footer">KORIMPIANO&STUDY © 2026 | Una creación de Yhissed Jiménez</div>', unsafe_allow_html=True)
