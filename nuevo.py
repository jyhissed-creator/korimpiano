import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORYM AI Piano Virtual")

piano_ia_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        body { background: #050008; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; }
        .header { padding: 10px; background: #111; border-bottom: 3px solid #6a00ff; text-align: center; }
        
        .ia-console { 
            background: #000; border: 2px solid #6a00ff; border-radius: 12px; 
            padding: 15px; width: 90%; margin: 10px auto;
        }
        #ia-orden { 
            width: 70%; padding: 10px; background: #111; color: #00ff88; 
            border: 1px solid #333; border-radius: 5px; outline: none;
        }
        .btn-enviar { padding: 10px 20px; background: #6a00ff; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }

        #piano-container { display: flex; justify-content: center; padding: 20px; background: #000; overflow-x: auto; }
        #piano { display: flex; height: 220px; position: relative; }
        .key-white { width: 45px; height: 100%; border: 1px solid #222; background: white; border-radius: 0 0 5px 5px; transition: 0.2s; position: relative; }
        .key-black { width: 28px; height: 130px; background: #222; margin-left: -14px; margin-right: -14px; z-index: 2; border-radius: 0 0 3px 3px; transition: 0.2s; }
        
        /* Efecto de toque de la IA */
        .ia-touch { background: #6a00ff !important; box-shadow: 0 0 40px #6a00ff, inset 0 -10px 20px #9b4dff !important; transform: translateY(5px); }
        .left-hand { background: #00ff88 !important; box-shadow: 0 0 30px #00ff88; } 
        .right-hand { background: #00aaff !important; box-shadow: 0 0 30px #00aaff; } 
        
        .note-label { position: absolute; bottom: 5px; width: 100%; text-align: center; color: #888; font-size: 10px; pointer-events: none; }
    </style>
</head>
<body>

<div class="header">
    <h2 style="margin:0; font-size: 20px;">🎹 KORYM AI SYSTEM</h2>
    <div class="ia-console">
        <input type="text" id="ia-orden" placeholder="Escribe: 'toca C', 'toca acorde do', 'limpiar'...">
        <button class="btn-enviar" onclick="ejecutarOrden()">ENVIAR</button>
        <div id="feedback-ia" style="margin-top:8px; color:#00ff88; font-family:monospace; font-size: 13px;">IA: Esperando orden...</div>
    </div>
    <input type="file" id="audioFile" accept="audio/*" style="margin:5px; font-size: 12px;">
    <audio id="player" controls style="width: 90%; height: 35px;"></audio>
</div>

<div id="piano-container">
    <div id="piano"></div>
</div>

<script>
    // Mapeo completo de notas para que la IA sepa qué tecla es cuál
    const pianoLayout = [
        {f: 261.63, n: "C"}, {f: 277.18, n: "C#", b:true}, {f: 293.66, n: "D"}, {f: 311.13, n: "D#", b:true},
        {f: 329.63, n: "E"}, {f: 349.23, n: "F"}, {f: 369.99, n: "F#", b:true}, {f: 392.00, n: "G"}, 
        {f: 415.30, n: "G#", b:true}, {f: 440.00, n: "A"}, {f: 466.16, n: "A#", b:true}, {f: 493.88, n: "B"},
        {f: 523.25, n: "C2"}, {f: 554.37, n: "C#2", b:true}, {f: 587.33, n: "D2"}, {f: 622.25, n: "D#2", b:true}
    ];

    const pianoDiv = document.getElementById('piano');
    let keysElements = [];

    pianoLayout.forEach((note, index) => {
        const div = document.createElement('div');
        div.className = note.b ? "key-black" : "key-white";
        div.innerHTML = `<span class="note-label">${note.n}</span>`;
        pianoDiv.appendChild(div);
        keysElements.push({ el: div, freq: note.f, name: note.n.toLowerCase() });
    });

    // --- EL CEREBRO DE ACCIÓN (Obedece tus órdenes) ---
    function ejecutarOrden() {
        const cmd = document.getElementById('ia-orden').value.toLowerCase();
        const fb = document.getElementById('feedback-ia');
        
        // Limpiar teclas antes de nueva orden
        keysElements.forEach(k => k.el.classList.remove('ia-touch'));

        if (cmd.includes("toca c") || cmd.includes("toca do")) {
            const tecla = keysElements.find(k => k.name === "c");
            if(tecla) tecla.el.classList.add('ia-touch');
            fb.innerText = "IA: Tocando nota DO (C) perfectamente.";
        } 
        else if (cmd.includes("acorde do") || cmd.includes("acorde c")) {
            // Un acorde son varias teclas a la vez: Do - Mi - Sol
            const notasAcorde = ["c", "e", "g"];
            keysElements.forEach(k => {
                if(notasAcorde.includes(k.name)) k.el.classList.add('ia-touch');
            });
            fb.innerText = "IA: Ejecutando Acorde de DO Mayor (C, E, G).";
        }
        else if (cmd.includes("limpiar") || cmd.includes("quitar")) {
            fb.innerText = "IA: Teclado reseteado.";
        }
        else {
            fb.innerText = "IA: No entiendo '" + cmd + "'. Intenta 'toca acorde do'.";
        }
    }

    // --- TU INVENTO ORIGINAL (Oído IA para archivos) ---
    document.getElementById('audioFile').onchange = function() {
        document.getElementById('player').src = URL.createObjectURL(this.files[0]);
        initAI();
    };

    function initAI() {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const source = audioCtx.createMediaElementSource(document.getElementById('player'));
        const analyser = audioCtx.createAnalyser();
        analyser.fftSize = 2048;
        source.connect(analyser);
        analyser.connect(audioCtx.destination);
        const dataArray = new Uint8Array(analyser.frequencyBinCount);

        function detect() {
            analyser.getByteFrequencyData(dataArray);
            // Solo quitamos las luces de "oído", no las de "órdenes"
            keysElements.forEach(k => k.el.classList.remove('left-hand', 'right-hand'));

            for (let i = 0; i < dataArray.length; i++) {
                if (dataArray[i] > 200) {
                    let f = (i * audioCtx.sampleRate / analyser.fftSize);
                    let closest = keysElements.reduce((p, c) => Math.abs(c.freq - f) < Math.abs(p.freq - f) ? c : p);
                    
                    if (closest.freq < 380) closest.el.classList.add('left-hand');
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

components.html(piano_ia_html, height=800, scrolling=False)
