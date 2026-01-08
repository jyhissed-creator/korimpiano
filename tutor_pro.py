<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>KORYM AI - Multi-Tonalidad</title>
    <style>
        body { background: #050505; color: white; font-family: 'Segoe UI', sans-serif; margin: 0; }
        .header { padding: 20px; background: #1a1a1a; border-bottom: 3px solid #6a00ff; }
        .controls { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin: 15px; }
        
        #piano { 
            display: flex; justify-content: center; height: 250px; 
            padding: 20px; background: #000; border-radius: 10px;
        }
        .key { 
            width: 45px; height: 100%; border: 1px solid #111; 
            background: white; position: relative; border-radius: 0 0 5px 5px;
        }
        /* Colores por mano */
        .left-hand { background: #3cff00 !important; box-shadow: inset 0 -20px 20px #2db300; } /* Verde */
        .right-hand { background: #00ccff !important; box-shadow: inset 0 -20px 20px #0086ad; } /* Azul */
        
        .note-name { color: #333; position: absolute; bottom: 10px; width: 100%; text-align: center; font-weight: bold; }
        select, input { padding: 8px; border-radius: 5px; border: none; }
        .legend { margin-top: 10px; font-size: 0.9em; }
    </style>
</head>
<body>

<div class="header">
    <h2>🎹 KORYM AI: Aprendizaje Inteligente</h2>
    <div class="controls">
        <div>
            <label>Audio:</label>
            <input type="file" id="audioFile" accept="audio/*">
        </div>
        <div>
            <label>Subir/Bajar Tono:</label>
            <select id="transpose">
                <option value="-2"> -2 Tonos (Bajar)</option>
                <option value="-1"> -1 Tono</option>
                <option value="0" selected>Tono Original</option>
                <option value="1">+1 Tono</option>
                <option value="2">+2 Tonos (Subir)</option>
            </select>
        </div>
    </div>
    <audio id="player" controls></audio>
    <div class="legend">
        <span style="color: #3cff00">● Mano Izquierda (Bajos)</span> | 
        <span style="color: #00ccff">● Mano Derecha (Melodía)</span>
    </div>
</div>

<div id="piano"></div>

<script>
    // Notas base para mapeo de frecuencias
    const baseNotes = [
        {f: 130.81, n: "C3"}, {f: 146.83, n: "D3"}, {f: 164.81, n: "E3"}, {f: 174.61, n: "F3"}, {f: 196.00, n: "G3"}, {f: 220.00, n: "A3"}, {f: 246.94, n: "B3"},
        {f: 261.63, n: "C4"}, {f: 293.66, n: "D4"}, {f: 329.63, n: "E4"}, {f: 349.23, n: "F4"}, {f: 392.00, n: "G4"}, {f: 440.00, n: "A4"}, {f: 493.88, n: "B4"},
        {f: 523.25, n: "C5"}, {f: 587.33, n: "D5"}, {f: 659.25, n: "E5"}, {f: 698.46, n: "F5"}, {f: 783.99, n: "G5"}, {f: 880.00, n: "A5"}, {f: 987.77, n: "B5"}
    ];

    const pianoDiv = document.getElementById('piano');
    const player = document.getElementById('player');
    const transposeSelect = document.getElementById('transpose');
    let keysElements = [];

    // Dibujar Piano
    baseNotes.forEach((note, index) => {
        const div = document.createElement('div');
        div.className = 'key';
        div.innerHTML = `<span class="note-name">${note.n}</span>`;
        pianoDiv.appendChild(div);
        keysElements.push({ el: div, freq: note.f, name: note.n });
    });

    document.getElementById('audioFile').onchange = function() {
        player.src = URL.createObjectURL(this.files[0]);
        startEngine();
    };

    function startEngine() {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const src = audioCtx.createMediaElementSource(player);
        const analyser = audioCtx.createAnalyser();
        
        src.connect(analyser);
        analyser.connect(audioCtx.destination);
        analyser.fftSize = 4096; // Mayor precisión para detectar notas

        const bufferLength = analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        function analyze() {
            analyser.getByteFrequencyData(dataArray);
            const transposeVal = parseInt(transposeSelect.value);

            // Limpiar todas las teclas
            keysElements.forEach(k => k.el.classList.remove('left-hand', 'right-hand'));

            // Escanear frecuencias activas
            for (let i = 0; i < bufferLength; i++) {
                if (dataArray[i] > 150) { // Umbral de volumen
                    let freq = i * audioCtx.sampleRate / analyser.fftSize;
                    
                    // Aplicar transposición (ajuste de frecuencia)
                    // Multiplicamos por 2^(semitonos/12)
                    let adjustedFreq = freq * Math.pow(2, -transposeVal / 12);

                    // Buscar la nota más cercana en nuestro piano
                    let closest = keysElements.reduce((prev, curr) => 
                        Math.abs(curr.freq - adjustedFreq) < Math.abs(prev.freq - adjustedFreq) ? curr : prev
                    );

                    // Lógica de manos:
                    // Si la frecuencia es baja (< 260Hz aprox), es Mano Izquierda
                    if (closest.freq < 260) {
                        closest.el.classList.add('left-hand');
                    } else {
                        closest.el.classList.add('right-hand');
                    }
                }
            }
            requestAnimationFrame(analyze);
        }

        player.onplay = () => { audioCtx.resume(); analyze(); };
    }
</script>
</body>
</html>
