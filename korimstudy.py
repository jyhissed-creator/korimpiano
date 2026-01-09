import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Korim.piano.&Studio")

st.markdown("""
    <style>
    .stApp { background: #010101; }
    iframe { border-radius: 20px; border: 1px solid #1a1a1a; box-shadow: 0 0 40px rgba(0,255,136,0.1); }
    </style>
""", unsafe_allow_html=True)

# SISTEMA OPERATIVO KORIM.PIANO.&STUDIO
korim_studio_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>
    <style>
        :root { --korim: #00ff88; --accent: #6a00ff; }
        body { background: #010101; color: #fff; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 15px; text-align: center; }
        
        .header-studio { margin-bottom: 25px; }
        .brand { font-size: 24px; font-weight: 900; letter-spacing: 2px; color: var(--korim); margin: 0; }
        .creator { font-size: 12px; letter-spacing: 5px; color: var(--accent); text-transform: uppercase; margin-top: 5px; font-weight: bold; }
        
        .console-box { background: #0a0a0a; border: 1px solid #222; border-radius: 20px; padding: 25px; max-width: 750px; margin: 0 auto; position: relative; overflow: hidden; }
        .console-box::before { content: ""; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: var(--korim); }
        
        textarea { width: 100%; height: 110px; background: #000; color: var(--korim); border: 1px solid #333; border-radius: 12px; padding: 15px; font-size: 16px; outline: none; transition: 0.3s; box-sizing: border-box; }
        textarea:focus { border-color: var(--korim); box-shadow: 0 0 15px rgba(0,255,136,0.2); }
        
        .controls-row { display: grid; grid-template-columns: 2fr 1fr; gap: 15px; margin-top: 15px; }
        button { padding: 16px; border-radius: 12px; border: none; font-weight: 900; cursor: pointer; text-transform: uppercase; transition: 0.2s; font-size: 14px; }
        
        .btn-boot { background: var(--accent); color: #fff; width: 100%; margin-bottom: 15px; box-shadow: 0 4px 15px rgba(106, 0, 255, 0.3); }
        .btn-exec { background: var(--korim); color: #000; }
        .btn-stop { background: #1a1a1a; color: #666; }
        
        #screen { background: #000; border-radius: 12px; padding: 20px; margin: 20px 0; text-align: left; font-size: 20px; border: 1px solid #111; min-height: 60px; color: #eee; }
        .chord-active { color: var(--korim); font-weight: 900; text-shadow: 0 0 10px var(--korim); }

        #piano-unit { overflow-x: auto; padding: 30px 0; display: flex; justify-content: center; }
        #piano { display: flex; height: 180px; position: relative; }
        .key { border: 1px solid #111; position: relative; transition: 0.1s; cursor: pointer; }
        .white { width: 45px; height: 100%; background: #fff; border-radius: 0 0 8px 8px; z-index: 1; }
        .black { width: 30px; height: 110px; background: #111; margin-left: -15px; margin-right: -15px; z-index: 2; border-radius: 0 0 5px 5px; border: 1px solid #333; }
        .pressed { background: var(--korim) !important; box-shadow: 0 0 30px var(--korim) !important; transform: translateY(5px); }
        
        .system-log { font-family: monospace; font-size: 10px; color: #444; margin-top: 10px; }
    </style>
</head>
<body>

    <div class="header-studio">
        <div class="brand">Korim.piano.&Studio</div>
        <div class="creator">BY YHISSED JIMÉNEZ</div>
    </div>

    <div class="console-box">
        <button class="btn-boot" id="boot-trigger" onclick="initStudio()">⚡ INICIALIZAR ESTUDIO</button>
        
        <textarea id="input-data" placeholder="Introduce la partitura... Ej: [C] SANTO [G] DIGNO [Am]"></textarea>
        
        <div class="controls-row">
            <button class="btn-exec" onclick="runProcess()">EJECUTAR SECUENCIA</button>
            <select id="transposer" style="background:#1a1a1a; color:white; border-radius:12px; border:1px solid #333; padding:10px;">
                <option value="0">Tono Original</option>
                <option value="2">+1 Tono</option>
                <option value="-2">-1 Tono</option>
            </select>
        </div>
        <button class="btn-stop" style="width:100%; margin-top:10px;" onclick="killProcess()">DETENER</button>
        <div class="system-log" id="status">KORIM_OS: STANDBY</div>
    </div>

    <div id="screen">Panel de visualización...</div>

    <div id="piano-unit">
        <div id="piano"></div>
    </div>

<script>
    // MOTOR DE AUDIO KORIM
    const sampler = new Tone.Sampler({
        urls: { C4: "C4.mp3", "D#4": "Ds4.mp3", "F#4": "Fs4.mp3", A4: "A4.mp3" },
        release: 1,
        baseUrl: "https://tonejs.github.io/audio/salamander/"
    }).toDestination();

    const dictionary = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const chordLibrary = { "M": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10] };
    const keyNodes = {};

    // GENERACIÓN DE HARDWARE VIRTUAL
    const pianoLayout = document.getElementById('piano');
    for (let oct = 3; oct <= 5; oct++) {
        dictionary.forEach(note => {
            const fullNote = note + oct;
            const key = document.createElement('div');
            key.className = `key ${note.includes('#') ? 'black' : 'white'}`;
            pianoLayout.appendChild(key);
            keyNodes[fullNote] = key;
        });
    }

    async function initStudio() {
        await Tone.start();
        document.getElementById('boot-trigger').innerText = "ESTUDIO ONLINE";
        document.getElementById('boot-trigger').style.background = "#0a0a0a";
        document.getElementById('boot-trigger').style.color = "var(--korim)";
        document.getElementById('boot-trigger').style.border = "1px solid var(--korim)";
        document.getElementById('status').innerText = "KORIM_OS: READY BY YHISSED JIMÉNEZ";
    }

    function killProcess() {
        Tone.Transport.stop();
        Tone.Transport.cancel();
        Object.values(keyNodes).forEach(k => k.classList.remove('pressed'));
    }

    function runProcess() {
        if (Tone.context.state !== 'running') return alert("Debe inicializar el estudio primero");
        killProcess();
        
        const content = document.getElementById('input-data').value;
        const shift = parseInt(document.getElementById('transposer').value);
        
        document.getElementById('screen').innerHTML = content.replace(/\\[(.*?)\\]/g, '<span class="chord-active">[$1]</span>');

        const sequence = [...content.matchAll(/\\[(.*?)\\]/g)];
        let timeClock = 0;

        sequence.forEach(step => {
            let chordName = step[1].toUpperCase();
            let root = chordName[0];
            if (chordName[1] === "#" || chordName[1] === "B") root = chordName.substring(0,2).replace("BB", "A#");
            let type = chordName.replace(root, "") || "M";

            let rootPos = dictionary.indexOf(root);
            if (rootPos !== -1) {
                let shiftedPos = (rootPos + shift + 12) % 12;
                let structure = chordLibrary[type] || chordLibrary["M"];
                
                structure.forEach(interval => {
                    let finalNote = dictionary[(shiftedPos + interval) % 12] + "4";
                    
                    sampler.triggerAttackRelease(finalNote, "2n", Tone.now() + timeClock);
                    
                    setTimeout(() => {
                        if(keyNodes[finalNote]) {
                            keyNodes[finalNote].classList.add('pressed');
                            setTimeout(() => keyNodes[finalNote].classList.remove('pressed'), 2000);
                        }
                    }, timeClock * 1000);
                });
                timeClock += 2.8; 
            }
        });
    }
</script>
</body>
</html>
"""

components.html(korim_studio_html, height=850)
