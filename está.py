import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORYM Perfect Piano")

st.markdown("""
    <style>
    .stApp { background-color: #020004; }
    iframe { border-radius: 25px; box-shadow: 0 0 60px #00ff8822; border: 1px solid #1a1a1a; }
    </style>
""", unsafe_allow_html=True)

perfect_piano_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>
    <style>
        :root { --neon: #00ff88; --accent: #6a00ff; }
        body { background: #020004; color: white; font-family: 'Segoe UI', Roboto, sans-serif; text-align: center; margin: 0; padding: 15px; overflow-x: hidden; }
        .creator { color: var(--accent); font-size: 11px; letter-spacing: 5px; font-weight: 800; text-transform: uppercase; margin-bottom: 15px; }
        
        /* Contenedor Pro */
        .panel { background: rgba(10, 10, 10, 0.95); border: 1px solid rgba(0, 255, 136, 0.3); border-radius: 20px; padding: 25px; max-width: 850px; margin: 0 auto; backdrop-filter: blur(10px); }
        
        textarea { width: 100%; height: 130px; background: #000; color: var(--neon); border: 1px solid #222; border-radius: 12px; padding: 15px; font-size: 15px; transition: 0.3s; resize: none; outline: none; box-sizing: border-box; }
        textarea:focus { border-color: var(--neon); box-shadow: 0 0 15px rgba(0, 255, 136, 0.1); }
        
        .controls { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 15px; margin: 20px 0; }
        select, button { padding: 14px; border-radius: 10px; border: none; font-weight: bold; cursor: pointer; transition: 0.2s; font-size: 14px; }
        
        .btn-unlock { background: linear-gradient(45deg, #ff4b00, #ff8800); color: white; grid-column: span 3; margin-bottom: 10px; box-shadow: 0 4px 15px rgba(255, 75, 0, 0.3); }
        .btn-unlock:active { transform: scale(0.98); }
        
        .btn-play { background: var(--accent); color: white; box-shadow: 0 4px 15px rgba(106, 0, 255, 0.3); }
        .btn-stop { background: #1a1a1a; color: #666; border: 1px solid #333; }
        .btn-play:hover { filter: brightness(1.2); }

        #display { background: #050505; border-radius: 15px; padding: 25px; margin: 20px 0; min-height: 100px; border-left: 6px solid var(--neon); text-align: left; font-size: 20px; line-height: 1.8; box-shadow: inset 0 0 20px rgba(0,0,0,1); }
        .chord-tag { color: var(--neon); font-weight: 900; background: rgba(0, 255, 136, 0.1); padding: 3px 8px; border-radius: 6px; border: 1px solid rgba(0, 255, 136, 0.2); margin: 0 2px; text-shadow: 0 0 10px rgba(0, 255, 136, 0.5); }

        /* Piano Luxury */
        #piano-container { overflow-x: auto; padding: 20px 0; cursor: pointer; }
        #piano { display: flex; justify-content: center; height: 180px; margin: 0 auto; width: max-content; }
        .key { border: 1px solid #111; flex-shrink: 0; position: relative; transition: all 0.1s ease; }
        .white { width: 45px; height: 100%; background: linear-gradient(to bottom, #eee 0%, #fff 100%); border-radius: 0 0 6px 6px; z-index: 1; }
        .black { width: 30px; height: 110px; background: linear-gradient(to bottom, #444 0%, #000 100%); margin-left: -15px; margin-right: -15px; z-index: 2; border-radius: 0 0 4px 4px; box-shadow: 0 5px 10px rgba(0,0,0,0.5); }
        
        .active { background: var(--neon) !important; transform: translateY(4px); box-shadow: 0 0 35px var(--neon) !important; }
        .key-label { position: absolute; bottom: 8px; width: 100%; text-align: center; color: #bbb; font-size: 10px; font-weight: bold; pointer-events: none; }
        
        #load-status { font-size: 12px; color: var(--neon); opacity: 0.7; margin-top: 10px; font-family: monospace; }
    </style>
</head>
<body>
    <div class="creator">KORYM Studio • YHISSED JIMÉNEZ</div>
    
    <div class="panel">
        <button id="unlock" class="btn-unlock" onclick="unlock()">🔓 INICIALIZAR MOTOR SINFÓNICO</button>
        <div id="load-status">SISTEMA OFFLINE</div>
        
        <textarea id="lyrics" placeholder="Escribe tu obra maestra aquí... [C] Ejemplo [G] de Acordes [Am]"></textarea>
        
        <div class="controls">
            <select id="shift" style="background:#111; color:white;">
                <optgroup label="Transportar">
                    <option value="0">Tono Original</option>
                    <option value="1">+1/2 (Sostenido)</option>
                    <option value="2">+1 (Tono)</option>
                    <option value="-1">-1/2 (Bemol)</option>
                    <option value="-2">-1 (Tono)</option>
                </optgroup>
            </select>
            <button class="btn-play" id="play-btn" onclick="play()" disabled>▶ TOCAR</button>
            <button class="btn-stop" onclick="stop()">⏹ PARAR</button>
        </div>
    </div>

    <div id="display">La partitura visual se generará aquí...</div>
    
    <div id="piano-container">
        <div id="piano"></div>
    </div>

<script>
    // Efectos de Perfección: Reverb y Limiter
    const reverb = new Tone.Reverb({ decay: 2.5, wet: 0.3 }).toDestination();
    const limiter = new Tone.Limiter(-1).connect(reverb);

    const pianoSampler = new Tone.Sampler({
        urls: {
            A0: "A0.mp3", C1: "C1.mp3", "D#1": "Ds1.mp3", "F#1": "Fs1.mp3",
            A1: "A1.mp3", C2: "C2.mp3", "D#2": "Ds2.mp3", "F#2": "Fs2.mp3",
            A2: "A2.mp3", C3: "C3.mp3", "D#3": "Ds3.mp3", "F#3": "Fs3.mp3",
            A3: "A3.mp3", C4: "C4.mp3", "D#4": "Ds4.mp3", "F#4": "Fs4.mp3",
            A4: "A4.mp3", C5: "C5.mp3", "D#5": "Ds5.mp3", "F#5": "Fs5.mp3",
            A5: "A5.mp3", C6: "C6.mp3"
        },
        release: 1.5,
        baseUrl: "https://tonejs.github.io/audio/salamander/"
    }).connect(limiter);

    const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const chordsMap = { 
        "M": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], 
        "maj7": [0, 4, 7, 11], "m7": [0, 3, 7, 10], "sus4": [0, 5, 7] 
    };
    const keysMap = {};

    // Piano Expandido (3 octavas para riqueza sonora)
    const pianoEl = document.getElementById('piano');
    for (let oct = 3; oct <= 5; oct++) {
        notes.forEach(n => {
            const note = n + oct;
            const div = document.createElement('div');
            div.className = `key ${n.includes('#') ? 'black' : 'white'}`;
            div.innerHTML = `<span class="key-label">${n}</span>`;
            pianoEl.appendChild(div);
            keysMap[note] = div;
            
            // Tocar con el mouse
            div.onmousedown = () => {
                if(Tone.context.state === 'running') {
                    pianoSampler.triggerAttack(note);
                    div.classList.add('active');
                }
            };
            div.onmouseup = () => {
                pianoSampler.triggerRelease(note);
                div.classList.remove('active');
            };
        });
    }

    async function unlock() {
        document.getElementById('load-status').innerText = "CALIBRANDO MUESTRAS...";
        await Tone.start();
        Tone.loaded().then(() => {
            document.getElementById('unlock').style.display = "none";
            document.getElementById('load-status').innerText = "ESTADO: CONCIERTO LISTO";
            document.getElementById('play-btn').disabled = false;
        });
    }

    function stop() {
        Tone.Transport.stop();
        Tone.Transport.cancel();
        Object.values(keysMap).forEach(k => k.classList.remove('active'));
    }

    function play() {
        stop();
        const text = document.getElementById('lyrics').value;
        const shift = parseInt(document.getElementById('shift').value);
        
        // Renderizado de lujo para la letra
        document.getElementById('display').innerHTML = text.replace(/\\[(.*?)\\]/g, '<span class="chord-tag">$1</span>');

        const matches = [...text.matchAll(/\\[(.*?)\\]/g)];
        let time = 0;

        matches.forEach(m => {
            let rawChord = m[1];
            // Lógica avanzada de detección de nota raíz
            let root = rawChord.charAt(0).toUpperCase();
            let remainder = rawChord.slice(1);
            
            if (remainder.charAt(0) === '#' || remainder.charAt(0).toLowerCase() === 'b') {
                root += remainder.charAt(0).replace('b', '#'); // Conversión simple
                remainder = remainder.slice(1);
            }
            
            let type = remainder || "M";
            let rootIdx = notes.indexOf(root.replace('Bb', 'A#').replace('Db', 'C#').replace('Eb', 'D#').replace('Gb', 'F#').replace('Ab', 'G#'));

            if (rootIdx !== -1) {
                let newIdx = (rootIdx + shift + 12) % 12;
                let intervals = chordsMap[type] || chordsMap["M"];
                
                intervals.forEach(i => {
                    let noteBase = (newIdx + i);
                    let octave = 4 + Math.floor(noteBase / 12);
                    let finalNote = notes[noteBase % 12] + octave;
                    
                    pianoSampler.triggerAttackRelease(finalNote, "1n", Tone.now() + time);
                    
                    setTimeout(() => {
                        if(keysMap[finalNote]) {
                            keysMap[finalNote].classList.add('active');
                            setTimeout(() => keysMap[finalNote].classList.remove('active'), 1500);
                        }
                    }, time * 1000);
                });
                time += 2.2; 
            }
        });
    }
</script>
</body>
</html>
"""

components.html(perfect_piano_html, height=900)
