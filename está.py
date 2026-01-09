import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORYM.PIANO Coach")

st.markdown("""
    <style>
    .stApp { background-color: #050008; }
    iframe { border-radius: 20px; box-shadow: 0 0 50px #6a00ff22; border: 1px solid #1a1a1a; }
    </style>
""", unsafe_allow_html=True)

piano_coach_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>
    <style>
        body { background: #050008; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 15px; text-align: center; }
        .header { color: #6a00ff; font-size: 11px; letter-spacing: 4px; font-weight: bold; margin-bottom: 5px; }
        .panel { background: #000; border: 1px solid #00ff88; border-radius: 15px; padding: 20px; max-width: 800px; margin: 0 auto; }
        
        textarea { width: 95%; height: 100px; background: #0a0a0a; color: #00ff88; border: 1px solid #333; border-radius: 8px; padding: 12px; margin-bottom: 15px; font-size: 14px; }
        
        .controls { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-bottom: 15px; }
        button { padding: 12px 20px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; transition: 0.3s; }
        .btn-init { background: #00ff88; color: #000; width: 100%; margin-bottom: 10px; }
        .btn-practice { background: #6a00ff; color: white; }
        
        #lyrics-coach { background: #070707; border-radius: 10px; padding: 20px; min-height: 60px; border-left: 5px solid #6a00ff; text-align: left; font-size: 18px; margin: 15px 0; }
        .current-chord { color: #00ff88; font-weight: bold; text-decoration: underline; }

        #piano { display: flex; justify-content: center; height: 160px; overflow-x: auto; padding: 20px 0; }
        .key { border: 1px solid #222; position: relative; transition: 0.2s; }
        .white { width: 40px; height: 100%; background: #fff; border-radius: 0 0 5px 5px; }
        .black { width: 26px; height: 100px; background: #222; margin-left: -13px; margin-right: -13px; z-index: 2; border-radius: 0 0 3px 3px; }
        .active { background: #00ff88 !important; box-shadow: 0 0 25px #00ff88 !important; }
        .guide { background: #6a00ff !important; box-shadow: 0 0 20px #6a00ff !important; }
    </style>
</head>
<body>
    <div class="header">YHISSED JIMÉNEZ PRESENTA</div>
    <h2>PIANO COACH PRO</h2>

    <button class="btn-init" onclick="init()">⚡ PASO 1: ACTIVAR AUDIO</button>

    <div class="panel">
        <textarea id="song-input" placeholder="Pega letra con acordes. Ejemplo: [C] Te doy [G] gracias..."></textarea>
        <div class="controls">
            <button class="btn-practice" onclick="startCoach()">▶️ EMPEZAR PRÁCTICA</button>
            <button style="background:#444; color:white;" onclick="stop()">DETENER</button>
        </div>
    </div>

    <div id="lyrics-coach">La letra aparecerá aquí...</div>
    <div id="piano"></div>

<script>
    const synth = new Tone.PolySynth(Tone.Synth).toDestination();
    const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const chordsMap = { "M": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10] };
    const pianoDiv = document.getElementById('piano');
    const keysMap = {};

    // Crear Piano (2 octavas)
    for (let oct = 3; oct <= 4; oct++) {
        notes.forEach(n => {
            const fullNote = n + oct;
            const div = document.createElement('div');
            div.className = `key ${n.includes('#') ? 'black' : 'white'}`;
            pianoDiv.appendChild(div);
            keysMap[fullNote] = div;
        });
    }

    async function init() {
        await Tone.start();
        document.querySelector('.btn-init').innerText = "✅ AUDIO CONECTADO";
        document.querySelector('.btn-init').style.background = "#222";
        document.querySelector('.btn-init').style.color = "#00ff88";
    }

    function stop() {
        Tone.Transport.stop();
        Tone.Transport.cancel();
        Object.values(keysMap).forEach(k => k.classList.remove('active', 'guide'));
    }

    function startCoach() {
        if (Tone.context.state !== 'running') return alert("Activa el audio primero");
        stop();
        
        const input = document.getElementById('song-input').value;
        const lyricsDiv = document.getElementById('lyrics-coach');
        
        // Procesar letra para mostrar
        lyricsDiv.innerHTML = input.replace(/\\[(.*?)\\]/g, '<span class="current-chord">[$1]</span>');

        const matches = [...input.matchAll(/\\[(.*?)\\]/g)];
        let time = 0;

        matches.forEach((match) => {
            let chordName = match[1].toUpperCase();
            let root = chordName[0];
            if (chordName[1] === "#" || chordName[1] === "B") root = chordName.substring(0, 2).replace("BB", "A#");
            let type = chordName.replace(root, "") || "M";

            let rootIdx = notes.indexOf(root);
            if (rootIdx !== -1) {
                let intervals = chordsMap[type] || chordsMap["M"];
                
                // Programar el sonido y la luz de guía
                intervals.forEach(inter => {
                    let noteName = notes[(rootIdx + inter) % 12] + "4";
                    
                    // Sonido
                    synth.triggerAttackRelease(noteName, "2n", Tone.now() + time);
                    
                    // Guía visual (se ilumina un poco antes y dura más)
                    setTimeout(() => {
                        if(keysMap[noteName]) {
                            keysMap[noteName].classList.add('guide');
                            setTimeout(() => keysMap[noteName].classList.remove('guide'), 2500);
                        }
                    }, time * 1000);
                });
                time += 3; // Tiempo más lento para practicar (3 segundos por acorde)
            }
        });
    }
</script>
</body>
</html>
"""

components.html(piano_coach_html, height=800)
