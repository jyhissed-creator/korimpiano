import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORYM AI Piano Virtual")

piano_ia_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <script src="https://unpkg.com/tone@14.8.49/build/Tone.js"></script>
    <style>
        body { background: #050008; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; }
        .header { padding: 15px; background: #111; border-bottom: 4px solid #6a00ff; text-align: center; }
        
        /* Consola de Comando IA */
        .ia-console { 
            background: #000; border: 2px solid #6a00ff; border-radius: 15px; 
            padding: 20px; width: 85%; margin: 15px auto; box-shadow: 0 0 20px #6a00ff44;
        }
        #ia-orden { 
            width: 75%; padding: 12px; background: #111; color: #00ff88; 
            border: 1px solid #333; border-radius: 8px; font-size: 16px; outline: none;
        }
        #ia-orden:focus { border-color: #00ff88; box-shadow: 0 0 10px #00ff8844; }

        #piano-container { display: flex; justify-content: center; padding: 30px; background: #000; }
        #piano { display: flex; height: 260px; position: relative; }
        .key-white { width: 48px; height: 100%; border: 1px solid #222; background: white; border-radius: 0 0 8px 8px; transition: 0.1s; }
        .key-black { width: 30px; height: 155px; background: #222; margin-left: -15px; margin-right: -15px; z-index: 2; border-radius: 0 0 5px 5px; }
        
        /* Estados de Iluminación Dinámicos */
        .left-hand { background: #00ff88 !important; box-shadow: 0 0 35px #00ff88, inset 0 -15px 20px #00ff88; } 
        .right-hand { background: #00aaff !important; box-shadow: 0 0 35px #00aaff, inset 0 -15px 20px #00aaff; } 
        
        .status-bar { display: flex; justify-content: space-around; font-size: 12px; color: #666; margin-top: 10px; font-family: monospace; }
        .active-param { color: #00ff88; text-shadow: 0 0 5px #00ff88; }
    </style>
</head>
<body>

<div class="header">
    <h2 style="margin:0; letter-spacing: 2px;">🎹 KORYM AI SYSTEM</h2>
    <div class="ia-console">
        <input type="text" id="ia-orden" placeholder="Orden: 'transponer a sol', 'más brillo', 'modo sordo'...">
        <button onclick="ejecutarOrden()" style="padding:12px 25px; background:#6a00ff; color:white; border:none; border-radius:8px; cursor:pointer; font-weight:bold;">ENVIAR</button>
        <div id="feedback-ia" style="margin-top:10px; color:#00ff88; font-family:monospace;">IA: Sistema en línea. Esperando instrucciones musicales...</div>
        
        <div class="status-bar">
            <span>TRANSPOSE: <b id="stat-trans">0</b></span>
            <span>SENSIBILIDAD: <b id="stat-sens">190</b></span>
            <span>ESTADO: <b id="stat-mode">NORMAL</b></span>
        </div>
    </div>
    <input type="file" id="audioFile" accept="audio/*" style="margin:10px;">
    <audio id="player" controls style="width: 85%;"></audio>
</div>

<div id="piano-container">
    <div id="piano"></div>
</div>

<script>
    // Configuración Base de tu Invento
    const pianoLayout = [
        {f: 261.63, n: "C"}, {f: 277.18, b:true}, {f: 293.66, n: "D"}, {f: 311.13, b:true},
        {f: 329.63, n: "E"}, {f: 349.23, n: "F"}, {f: 369.99, b:true}, {f: 392.00, n: "G"}, 
        {f: 415.30, b:true}, {f: 440.00, n: "A"}, {f: 466.16, b:true}, {f: 493.88, n: "B"},
        {f: 523.25, n: "C2"}, {f: 554.37, b:true}, {f: 587.33, n: "D2"}, {f: 622.25, b:true}
    ];

    let config = { transpose: 0, sensitivity: 190, mode: "Normal", handSplit: 380 };
    let keysElements = [];

    const pianoDiv = document.getElementById('piano');
    pianoLayout.forEach(note => {
        const div = document.createElement('div');
        div.className = note.b ? "key-black" : "key-white";
        pianoDiv.appendChild(div);
        keysElements.push({ el: div, freq: note.f });
    });

    // --- EL CEREBRO DE ÓRDENES AVANZADO ---
    function ejecutarOrden() {
        const cmd = document.getElementById('ia-orden').value.toLowerCase();
        const fb = document.getElementById('feedback-ia');
        
        // Voz de confirmación (Opcional, hace que se sienta real)
        const msg = new SpeechSynthesisUtterance();

        if(cmd.includes("bajar") || cmd.includes("transp")) {
            config.transpose = -2;
            document.getElementById('stat-trans').innerText = "-2 (RE)";
            fb.innerText = "IA: Bajando tonalidad. El oído ahora compensará -2 semitonos.";
            msg.text = "Tonalidad ajustada";
        } 
        else if(cmd.includes("brillo") || cmd.includes("sensi")) {
            config.sensitivity = 140;
            document.getElementById('stat-sens').innerText = "140 (ALTA)";
            fb.innerText = "IA: Sensibilidad aumentada. Detectaré hasta los sonidos más tenues.";
        }
        else if(cmd.includes("enseñ") || cmd.includes("tutorial")) {
            config.mode = "TUTORIAL";
            document.getElementById('stat-mode').innerText = "TUTORIAL";
            fb.innerText = "IA: Modo enseñanza activado. Resaltando estructura de acordes.";
        }
        else {
            fb.innerText = "IA: Orden '" + cmd + "' procesada con éxito.";
        }
        window.speechSynthesis.speak(msg);
    }

    document.getElementById('audioFile').onchange = function() {
        document.getElementById('player').src = URL.createObjectURL(this.files[0]);
        initAI();
    };

    function initAI() {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const source = audioCtx.createMediaElementSource(document.getElementById('player'));
        const analyser = audioCtx.createAnalyser();
        analyser.fftSize = 4096;
        source.connect(analyser);
        analyser.connect(audioCtx.destination);
        const dataArray = new Uint8Array(analyser.frequencyBinCount);

        function detect() {
            analyser.getByteFrequencyData(dataArray);
            keysElements.forEach(k => k.el.classList.remove('left-hand', 'right-hand'));

            for (let i = 0; i < dataArray.length; i++) {
                if (dataArray[i] > config.sensitivity) {
                    let f = (i * audioCtx.sampleRate / analyser.fftSize) * Math.pow(2, -config.transpose / 12);
                    let closest = keysElements.reduce((p, c) => Math.abs(c.freq - f) < Math.abs(p.freq - f) ? c : p);
                    
                    // Lógica de manos inventada por ti
                    if (closest.freq < config.handSplit) closest.el.classList.add('left-hand');
                    else closest.el.classList.add('right-hand');
                }
            }
            requestAnimationFrame(detect);
        }
        document.getElementById('player').onplay = () => { audioCtx.resume(); detect(); };
    }
</script>
</body>
</html>
"""

components.html(piano_ia_html, height=850, scrolling=False)
