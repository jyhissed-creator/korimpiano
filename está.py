import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORYM.PIANO Lyrics & Chords")

st.markdown("""
    <style>
    .stApp { background-color: #050008; }
    footer {visibility: hidden;}
    iframe { border-radius: 20px; box-shadow: 0 0 40px #6a00ff44; border: 1px solid #1a1a1a; }
    </style>
""", unsafe_allow_html=True)

piano_lyrics_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://unpkg.com/tone@14.8.49/build/Tone.js"></script>
    <style>
        body { background: #050008; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 15px; text-align: center; }
        .creator-tag { font-size: 11px; color: #6a00ff; letter-spacing: 4px; font-weight: bold; margin-bottom: 5px; }
        .system-title { font-size: 24px; font-weight: 800; color: #fff; margin-bottom: 20px; }
        
        .main-container { display: flex; flex-direction: column; gap: 20px; max-width: 900px; margin: 0 auto; }
        .input-area { background: #000; border: 1px solid #00ff88; border-radius: 15px; padding: 20px; }
        
        textarea { width: 95%; height: 150px; background: #0a0a0a; color: #00ff88; border: 1px solid #333; border-radius: 8px; padding: 10px; font-size: 14px; margin-bottom: 15px; resize: vertical; outline: none; }
        
        .controls { display: flex; gap: 15px; justify-content: center; align-items: center; flex-wrap: wrap; margin-bottom: 10px; }
        select, button { padding: 12px 20px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; }
        
        .btn-play { background: #00ff88; color: #000; }
        .btn-stop { background: #ff3333; color: white; }
        
        #lyrics-display { background: #0a0a0a; border-radius: 10px; padding: 20px; min-height: 100px; border-left: 4px solid #6a00ff; text-align: left; line-height: 1.6; color: #eee; white-space: pre-wrap; margin: 10px 0; font-size: 18px; }
        .chord-highlight { color: #00ff88; font-weight: bold; font-family: monospace; background: #00ff8811; padding: 2px 4px; border-radius: 4px; }
        
        #piano-container { display: flex; justify-content: center; overflow-x: auto; padding: 20px 0; }
        #piano { display: flex; position: relative; height: 160px; }
        .key { position: relative; border: 1px solid #222; transition: 0.1s; }
        .white { width: 35px; height: 100%; background: #fff; border-radius: 0 0 5px 5px; z-index: 1; }
        .black { width: 22px; height: 100px; background: #222; margin-left: -11px; margin-right: -11px; z-index: 2; border-radius: 0 0 3px 3px; }
        .active { background: #00ff88 !important; box-shadow: 0 0 20px #00ff88 !important; }
    </style>
</head>
<body>

    <div class="creator-tag">YHISSED JIMÉNEZ PRESENTA</div>
    <div class="system-title">KORYM.PIANO: LYRICS & CHORDS PRO</div>

    <div class="main-container">
        <div class="input-area">
            <textarea id="full-song" placeholder="Pega aquí la letra con acordes. Ejemplo:&#10;[C] Cielito [G] lindo [C] siempre..."></textarea>
            
            <div class="controls">
                <div>
                    <span style="font-size: 12px;">TONALIDAD:</span>
                    <select id="transpose-val">
                        <option value="0">Original</option>
                        <option value="2">+1 Tono</option>
                        <option value="-2">-1 Tono</option>
                        <option value="1">+1/2 Tono</option>
                        <option value="-1">-1/2 Tono</option>
                    </select>
                </div>
                <button class="btn-play" onclick="reproducirMusica()">REPRODUCIR CANCIÓN</button>
                <button class="btn-stop" onclick="detenerTodo()">PARAR</button>
            </div>
        </div>

        <div id="lyrics-display">La letra procesada aparecerá aquí mientras suena...</div>

        <div id="piano-container"><div id="piano"></div></div>
    </div>

<script>
    const synth = new Tone.PolySynth(Tone.Synth).toDestination();
    const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const chordsMap = { "M": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "m7": [0, 3, 7, 10] };
    const keysData = [];

    // Crear Piano
    const piano = document.getElementById('piano');
    for (let oct = 3; oct <= 5; oct++) {
        notes.forEach(n => {
            const fullNote = n + oct;
            const div = document.createElement('div');
            div.className = `key ${n.includes("#") ? 'black' : 'white'}`;
            piano.appendChild(div);
            keysData.push({ el: div, note: fullNote, simple: n });
        });
    }

    function detenerTodo() {
        Tone.Transport.stop();
        Tone.Transport.cancel();
        keysData.forEach(k => k.el.classList.remove('active'));
    }

    async function reproducirMusica() {
        await Tone.start();
        detenerTodo();
        
        const rawText = document.getElementById('full-song').value;
        const display = document.getElementById('lyrics-display');
        const shift = parseInt(document.getElementById('transpose-val').value);
        
        // Resaltar acordes visualmente en la letra
        let highlightedText = rawText.replace(/\\[(.*?)\\]/g, '<span class="chord-highlight">$1</span>');
        display.innerHTML = highlightedText;

        // Extraer acordes para tocar
        const matches = rawText.matchAll(/\\[(.*?)\\]/g);
        let time = 0;

        for (const match of matches) {
            let chordName = match[1].toUpperCase();
            let root = chordName[0];
            if (chordName[1] === "#" || chordName[1] === "B") root = chordName.substring(0, 2).replace("BB", "A#");
            let type = chordName.replace(root, "") || "M";

            let rootIdx = notes.indexOf(root);
            if (rootIdx !== -1) {
                let transIdx = (rootIdx + shift + 12) % 12;
                let intervals = chordsMap[type] || chordsMap["M"];
                
                intervals.forEach(inter => {
                    let noteName = notes[(transIdx + inter) % 12];
                    tocar(noteName + "4", time);
                });
                time += 2; // Tiempo entre cada acorde de la letra
            }
        }
    }

    function tocar(n, time) {
        synth.triggerAttackRelease(n, "2n", Tone.now() + time);
        const key = keysData.find(k => k.note === n);
        if(key) {
            setTimeout(() => key.el.classList.add('active'), time * 1000);
            setTimeout(() => key.el.classList.remove('active'), (time * 1000) + 800);
        }
    }
</script>
</body>
</html>
"""

components.html(piano_lyrics_html, height=900, scrolling=True)
