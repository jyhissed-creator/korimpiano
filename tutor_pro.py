<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>KORYM AI - Piano Virtual Real</title>
    <style>
        body { background: #0a0a0a; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; overflow-x: hidden; }
        .header { padding: 20px; background: #111; border-bottom: 4px solid #6a00ff; text-align: center; }
        
        /* Contenedor del Piano */
        #piano-container { 
            position: relative; display: flex; justify-content: center; 
            padding: 50px 20px; background: #000; margin-top: 20px;
        }
        
        #piano { display: flex; position: relative; height: 280px; }

        /* Teclas Blancas */
        .key-white { 
            width: 50px; height: 100%; border: 1px solid #ccc; 
            background: white; border-radius: 0 0 8px 8px; position: relative; z-index: 1;
        }

        /* Teclas Negras */
        .key-black { 
            width: 30px; height: 160px; background: #222; 
            margin-left: -15px; margin-right: -15px; z-index: 2; border-radius: 0 0 5px 5px;
        }

        /* Iluminación por manos */
        .left-hand { background: #3cff00 !important; box-shadow: 0 0 30px #3cff00; } /* Verde */
        .right-hand { background: #00ccff !important; box-shadow: 0 0 30px #00ccff; } /* Azul */
        
        .note-name { 
            position: absolute; bottom: 10px; width: 100%; text-align: center; 
            color: #888; font-size: 12px; font-weight: bold; pointer-events: none;
        }

        .controls { display: flex; justify-content: center; gap: 15px; margin: 15px; flex-wrap: wrap; }
        select, input { padding: 10px; border-radius: 5px; border: none; background: #222; color: white; }
        .legend { font-size: 14px; margin-top: 10px; color: #aaa; }
    </style>
</head>
<body>

<div class="header">
    <h2>🎹 KORYM AI PIANO</h2>
    <div class="controls">
        <input type="file" id="audioFile" accept="audio/*">
        <select id="transpose">
            <option value="-2">Bajar -2 Tonos</option>
            <option value="0" selected>Tono Original</option>
            <option value="2">Subir +2 Tonos</option>
        </select>
    </div>
    <audio id="player" controls></audio>
    <div class="legend">
        🟩 Izquierda (Bajos) | 🟦 Derecha (Melodía)
    </div>
</div>

<div id="piano-container">
    <div id="piano"></div>
</div>

<script>
    // Estructura de un piano de 2 octavas con frecuencias
    const pianoLayout = [
        {f: 261.63, n: "C", t: "W"}, {f: 277.18, n: "C#", t: "B"},
        {f: 293.66, n: "D", t: "W"}, {f: 311.13, n: "D#", t: "B"},
        {f: 329.63, n: "E", t: "W"},
        {f: 349.23, n: "F", t: "W"}, {f: 369.99, n: "F#", t: "B"},
        {f: 392.00, n: "G", t: "W"}, {f: 415.30, n: "G#", t: "B"},
        {f: 440.00, n: "A", t: "W"}, {f: 466.16, n: "A#", t: "B"},
        {f: 493.88, n: "B", t: "W"},
        {f: 523.25, n: "C2", t: "W"}, {f: 554.37, n: "C#2", t: "B"},
        {f: 587.33, n: "D2", t: "W"}, {f: 622.25, n: "D#2", t: "B"},
        {f: 659.25, n: "E2", t: "W"},
        {f: 698.46, n: "F2", t: "W"}, {f: 739.99, n: "F#2", t: "B"},
        {f: 783.99, n: "G2", t: "W"}, {f: 830.61, n: "G#2", t: "B"},
        {f: 880.00, n: "A2", t: "W"}, {f: 932.33, n: "A#2", t: "B"},
        {f: 987.77, n: "B2", t: "W"}
    ];

    const pianoDiv = document.getElementById('piano');
    const player = document.getElementById('player');
    let keysElements = [];

    // Dibujar Piano Real
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
        analyser.fftSize = 8192; // Alta resolución

        source.connect(analyser);
        analyser.connect(audioCtx.destination);

        const dataArray = new Uint8Array(analyser.frequencyBinCount);

        function detect() {
            analyser.getByteFrequencyData(dataArray);
            const transpose = parseInt(document.getElementById('transpose').value);

            keysElements.forEach(k => k.el.classList.remove('left-hand', 'right-hand'));

            for (let i = 0; i < dataArray.length; i++) {
                if (dataArray[i] > 180) { // Sensibilidad
                    let detectedFreq = i * audioCtx.sampleRate / analyser.fftSize;
                    let transposedFreq = detectedFreq * Math.pow(2, -transpose / 12);

                    let closest = keysElements.reduce((prev, curr) => 
                        Math.abs(curr.freq - transposedFreq) < Math.abs(prev.freq - transposedFreq) ? curr : prev
                    );

                    // Lógica de manos mejorada
                    if (closest.freq < 350) closest.el.classList.add('left-hand');
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
