import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="KORYM Master Piano")

# CSS para ocultar el exceso de Streamlit y centrar la experiencia
st.markdown("""
    <style>
    .stApp { background: #000; }
    iframe { border: none !important; border-radius: 20px; }
    </style>
""", unsafe_allow_html=True)

# EL ALGORITMO MAESTRO (HTML5 + Tone.js + Transposer Logic)
master_algo_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>
    <style>
        :root { --neon: #00ff88; --bg: #050505; }
        body { background: var(--bg); color: white; font-family: 'Segoe UI', sans-serif; margin: 0; padding: 10px; text-align: center; }
        
        .panel-control { background: #111; border: 1px solid #222; border-radius: 15px; padding: 15px; margin-bottom: 10px; }
        textarea { width: 100%; height: 80px; background: #000; color: var(--neon); border: 1px solid #333; border-radius: 10px; padding: 10px; font-size: 14px; box-sizing: border-box; }
        
        .grid-btns { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 10px; }
        button { padding: 12px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; font-size: 14px; }
        
        .btn-init { background: #ff4b00; color: white; grid-column: span 2; }
        .btn-play { background: #6a00ff; color: white; }
        .btn-stop { background: #333; color: white; }
        
        #pantalla { background: #000; border-left: 4px solid var(--neon); padding: 15px; margin: 15px 0; text-align: left; min-height: 60px; font-size: 18px; border-radius: 0 10px 10px 0; }
        .acorde-v { color: var(--neon); font-weight: bold; text-shadow: 0 0 5px var(--neon); }

        /* Piano Optimizado para Táctil */
        #piano-wrap { overflow-x: auto; white-space: nowrap; padding: 10px 0; -webkit-overflow-scrolling: touch; }
        #piano { display: inline-flex; position: relative; height: 150px; }
        .key { border: 1px solid #111; position: relative; transition: 0.1s; display: inline-block; }
        .white { width: 42px; height: 100%; background: #fff; border-radius: 0 0 5px 5px; }
        .black { width: 28px; height: 95px; background: #000; margin-left: -14px; margin-right: -14px; z-index: 2; border-radius: 0 0 3px 3px; border: 1px solid #333; }
        .active { background: var(--neon) !important; box-shadow: 0 0 20px var(--neon) !important; transform: translateY(5px); }
        
        #loading { font-size: 11px; color: #555; margin-top: 5px; }
    </style>
</head>
<body>

    <div style="color:#6a00ff; font-weight:bold; letter-spacing:2px; font-size:12px;">KORYM ENGINE v3.0</div>
    
    <div class="panel-control">
        <button id="btn-on" class="btn-init" onclick="encender()">⚡ 1. ENCENDER SISTEMA</button>
        <div id="loading">Estado: Esperando activación...</div>
        
        <textarea id="song-input" placeholder="Ej: [C] Dios [G] de [Am] amor..."></textarea>
        
        <div style="margin: 10px 0;">
            <label style="font-size:12px; color:#888;">Transportar:</label>
            <select id="trans-val" style="background:#222; color:white; border:none; padding:5px; border-radius:5px;">
                <option value="0">Tono Original</option>
                <option value="2">+1 Tono</option>
                <option value="-2">-1 Tono</option>
            </select>
        </div>

        <div class="grid-btns">
            <button class="btn-play" onclick="reproducir()">▶ PRACTICAR</button>
            <button class="btn-stop" onclick="parar()">🛑 PARAR</button>
        </div>
    </div>

    <div id="pantalla">Letra y guía...</div>

    <div id="piano-wrap">
        <div id="piano"></div>
    </div>

<script>
    // EL ALGORITMO DE AUDIO
    const synth = new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: "triangle" },
        envelope: { attack: 0.05, release: 1 }
    }).toDestination();

    const notas = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const mapaAcordes = { "M": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10] };
    const teclasRef = {};

    // Dibujar Piano (3 Octavas para mayor rango)
    const pianoDiv = document.getElementById('piano');
    for (let oct = 3; oct <= 5; oct++) {
        notas.forEach(n => {
            const notaID = n + oct;
            const k = document.createElement('div');
            k.className = `key ${n.includes('#') ? 'black' : 'white'}`;
            pianoDiv.appendChild(k);
            teclasRef[notaID] = k;
        });
    }

    async function encender() {
        await Tone.start();
        document.getElementById('btn-on').innerText = "✅ SISTEMA ACTIVO";
        document.getElementById('btn-on').style.background = "#222";
        document.getElementById('loading').innerText = "Audio desbloqueado. Listo para tocar.";
    }

    function parar() {
        Tone.Transport.stop();
        Tone.Transport.cancel();
        Object.values(teclasRef).forEach(t => t.classList.remove('active'));
    }

    function reproducir() {
        if (Tone.context.state !== 'running') {
            alert("Presiona el botón naranja 'ENCENDER' primero.");
            return;
        }
        parar();
        
        const raw = document.getElementById('song-input').value;
        const trans = parseInt(document.getElementById('trans-val').value);
        
        // Algoritmo de visualización de letra
        document.getElementById('pantalla').innerHTML = raw.replace(/\\[(.*?)\\]/g, '<span class="acorde-v">[$1]</span>');

        const matches = [...raw.matchAll(/\\[(.*?)\\]/g)];
        let delay = 0;

        matches.forEach(m => {
            let chordStr = m[1].toUpperCase();
            let root = chordStr[0];
            if (chordStr[1] === "#" || chordStr[1] === "B") root = chordStr.substring(0,2).replace("BB", "A#");
            let type = chordStr.replace(root, "") || "M";

            let rootIdx = notas.indexOf(root);
            if (rootIdx !== -1) {
                // Algoritmo de Transposición
                let transIdx = (rootIdx + trans + 12) % 12;
                let intervalos = mapaAcordes[type] || mapaAcordes["M"];
                
                intervalos.forEach(i => {
                    let nFinal = notas[(transIdx + i) % 12] + "4";
                    
                    // Disparo de Audio y Luz sincronizado
                    synth.triggerAttackRelease(nFinal, "2n", Tone.now() + delay);
                    
                    setTimeout(() => {
                        if(teclasRef[nFinal]) {
                            teclasRef[nFinal].classList.add('active');
                            setTimeout(() => teclasRef[nFinal].classList.remove('active'), 1500);
                        }
                    }, delay * 1000);
                });
                delay += 3; // Ritmo de aprendizaje (3 seg por acorde)
            }
        });
    }
</script>
</body>
</html>
"""

components.html(master_algo_html, height=800, scrolling=False)
