import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORYM AI Piano Virtual")

piano_ia_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <style>
        body { background: #0a0a0a; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; }
        .header { padding: 15px; background: #111; border-bottom: 4px solid #6a00ff; text-align: center; }
        
        /* Caja de Órdenes IA */
        .ia-input-container { padding: 10px; background: #1a1a1a; border-radius: 10px; margin: 10px auto; width: 80%; border: 1px solid #333; }
        #ia-orden { width: 70%; padding: 10px; background: #000; color: #00ff88; border: 1px solid #444; border-radius: 5px; font-family: monospace; }
        .btn-ia { padding: 10px 20px; background: #6a00ff; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }

        #piano-container { display: flex; justify-content: center; padding: 40px 10px; background: #000; }
        #piano { display: flex; position: relative; height: 250px; }
        .key-white { width: 45px; height: 100%; border: 1px solid #ccc; background: white; border-radius: 0 0 8px 8px; position: relative; }
        .key-black { width: 28px; height: 150px; background: #222; margin-left: -14px; margin-right: -14px; z-index: 2; border-radius: 0 0 5px 5px; }
        .left-hand { background: #3cff00 !important; box-shadow: 0 0 30px #3cff00; } 
        .right-hand { background: #00ccff !important; box-shadow: 0 0 30px #00ccff; } 
        #estado-ia { color: #00ff88; font-size: 14px; margin-top: 5px; font-family: monospace; }
    </style>
</head>
<body>

<div class="header">
    <h2 style="margin:0;">🎹 KORYM AI PIANO</h2>
    
    <div class="ia-input-container">
        <input type="text" id="ia-orden" placeholder="Escribe tu orden (ej: bajar 2 tonos, modo enseñanza, verde más brillo)...">
        <button class="btn-ia" onclick="procesarOrdenIA()">🧠 Ejecutar</button>
        <div id="estado-ia">Esperando órdenes...</div>
    </div>

    <input type="file" id="audioFile" accept="audio/*">
    <audio id="player" controls style="width: 80%; margin-top:10px;"></audio>
</div>

<div id="piano-container">
    <div id="piano"></div>
</div>

<script>
    const pianoLayout = [
        {f: 261.63, n: "C"}, {f: 277.18, n: "C#", b:true}, {f: 293.66, n: "D"}, {f: 311.13, n: "D#", b:true},
        {f: 329.63, n: "E"}, {f: 349.23, n: "F"}, {f: 369.99, n: "F#", b:true}, {f: 392.00, n: "G"}, 
        {f: 415.30, n: "G#", b:true}, {f: 440.00, n: "A"}, {f: 466.16, n: "A#", b:true}, {f: 493.88, n: "B"},
        {f: 523.25, n: "C2"}, {f: 554.37, n: "C#2", b:true}, {f: 587.33, n: "D2"}, {f: 622.25, n: "D#2", b:true}
    ];

    let currentTranspose = 0;
    let sensitivity = 190;
    const pianoDiv = document.getElementById('piano');
    let keysElements = [];

    pianoLayout.forEach(note => {
        const div = document.createElement('div');
        div.className = note.b ? "key-black" : "key-white";
        pianoDiv.appendChild(div);
        keysElements.push({ el: div, freq: note.f });
    });

    // --- EL CEREBRO DE ÓRDENES (TU INVENCIÓN) ---
    function procesarOrdenIA() {
        const input = document.getElementById('ia-orden').value.toLowerCase();
        const estado = document.getElementById('estado-ia');
        
        if(input.includes("bajar") || input.includes("transponer a re")) {
            currentTranspose = -2;
            estado.innerText = "SISTEMA: Tonalidad ajustada a -2 semitonos (Re).";
        } else if(input.includes("subir") || input.includes("original")) {
            currentTranspose = 0;
            estado.innerText = "SISTEMA: Volviendo a tono original.";
        } else if(input.includes("sensibilidad")) {
            sensitivity = 150;
            estado.innerText = "SISTEMA: Oído IA ajustado para sonidos suaves.";
        } else {
            estado.innerText = "SISTEMA: Orden recibida. Analizando contexto...";
        }
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
                if (dataArray[i] > sensitivity) {
                    let f = (i * audioCtx.sampleRate / analyser.fftSize) * Math.pow(2, -currentTranspose / 12);
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

components.html(piano_ia_html, height=850, scrolling=False)
