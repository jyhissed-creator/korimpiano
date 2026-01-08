import streamlit as st
import streamlit.components.v1 as components

# 1. Configuración de la App
st.set_page_config(layout="wide", page_title="KORYM AI Piano Virtual")

# 2. Tu invento: IA de Oído y Cerebro Polifónico (Integrado en HTML/JS)
# Esto permite que la IA corra en el celular del usuario (Costo $0 para ti)
piano_ia_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>KORYM AI - Piano Virtual Real</title>
    <style>
        body { background: #0a0a0a; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; overflow: hidden; }
        .header { padding: 15px; background: #111; border-bottom: 4px solid #6a00ff; text-align: center; }
        
        #piano-container { 
            position: relative; display: flex; justify-content: center; 
            padding: 40px 10px; background: #000;
        }
        
        #piano { display: flex; position: relative; height: 250px; }

        .key-white { 
            width: 45px; height: 100%; border: 1px solid #ccc; 
            background: white; border-radius: 0 0 8px 8px; position: relative; z-index: 1;
        }

        .key-black { 
            width: 28px; height: 150px; background: #222; 
            margin-left: -14px; margin-right: -14px; z-index: 2; border-radius: 0 0 5px 5px;
        }

        /* Tu lógica de manos: Verde Izquierda / Azul Derecha */
        .left-hand { background: #3cff00 !important; box-shadow: 0 0 30px #3cff00; } 
        .right-hand { background: #00ccff !important; box-shadow: 0 0 30px #00ccff; } 
        
        .note-name { 
            position: absolute; bottom: 10px; width: 100%; text-align: center; 
            color: #888; font-size: 11px; font-weight: bold; pointer-events: none;
        }

        .controls { display: flex; justify-content: center; gap: 10px; margin: 10px; flex-wrap: wrap; }
        input, select { padding: 8px; border-radius: 5px; background: #222; color: white; border: 1px solid #444; }
    </style>
</head>
<body>

<div class="header">
    <h2 style="margin:0;">🎹 KORYM AI PIANO</h2>
    <div class="controls">
        <input type="file" id="audioFile" accept="audio/*">
        <select id="transpose">
            <option value="-2">Bajar -2 (Re)</option>
            <option value="0" selected>Tono Original</option>
            <option value="2">Subir +2 (Mi)</option>
        </select>
    </div>
    <audio id="player" controls style="width: 80%;"></audio>
</div>

<div id="piano-container">
    <div id="piano"></div>
</div>

<script>
    // Tu mapa de frecuencias para que la IA "entienda" qué tecla brilla
    const pianoLayout = [
        {f: 261.63, n: "C", t: "W"}, {f: 277.18, n: "C#", t: "B"},
        {f: 293.66, n: "D", t: "W"}, {f: 311.13, n: "D#", t: "B"},
        {f: 329.63, n: "E", t: "W"}, {f: 349.23, n: "F", t: "W"}, 
        {f: 369.99, n: "F#", t: "B"}, {f: 392.00, n: "G", t: "W"}, 
        {f: 415.30, n: "G#", t: "B"}, {f: 440.00, n: "A", t: "W"}, 
        {f: 466.16, n: "A#", t: "B"}, {f: 493.88, n: "B", t: "W"},
        {f: 523.25, n: "C2", t: "W"}, {f: 554.37, n: "C#2", t: "B"},
        {f: 587.33, n: "D2", t: "W"}, {f: 622.25, n: "D#2", t: "B"},
        {f: 659.25, n: "E2", t: "W"}
    ];

    const pianoDiv = document.getElementById('piano');
    const player = document.getElementById('player');
    let keysElements = [];

    // Dibujar el teclado profesional
    pianoLayout.forEach(note => {
        const div = document.createElement('div');
        div.className = note.t === "W" ? "key-white" : "key-black";
        div.innerHTML = `<span class="note-name">${note.n}</span>`;
        pianoDiv.appendChild(div);
        keysElements.push({ el: div, freq: note.f });
    });

    document.getElementById('audioFile').onchange = function() {
        player.src = URL.createObjectURL(this.files[0]);
        initAI();
    };

    function initAI() {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const source = audioCtx.createMediaElementSource(player);
        const analyser = audioCtx.createAnalyser();
        analyser.fftSize = 4096;

        source.connect(analyser);
        analyser.connect(audioCtx.destination);

        const dataArray = new Uint8Array(analyser.frequencyBinCount);

        function detect() {
            analyser.getByteFrequencyData(dataArray);
            const transp = parseInt(document.getElementById('transpose').value);

            keysElements.forEach(k => k.el.classList.remove('left-hand', 'right-hand'));

            for (let i = 0; i < dataArray.length; i++) {
                if (dataArray[i] > 190) { // Sensibilidad del "oído"
                    let detectedFreq = i * audioCtx.sampleRate / analyser.fftSize;
                    let transposedFreq = detectedFreq * Math.pow(2, -transp / 12);

                    let closest = keysElements.reduce((prev, curr) => 
                        Math.abs(curr.freq - transposedFreq) < Math.abs(prev.freq - transposedFreq) ? curr : prev
                    );

                    // Lógica de separación de manos (Inventada por ti)
                    if (closest.freq < 380) closest.el.classList.add('left-hand');
                    else closest.el.classList.add('right-hand');
                }
            }
            requestAnimationFrame(detect);
        }
        player.onplay = () => { audioCtx.resume(); detect(); };
    }
</script>
</body>
</html>
"""

# 3. Lanzar la app (Esto conecta tu HTML con Streamlit)
components.html(piano_ia_html, height=800, scrolling=False)
