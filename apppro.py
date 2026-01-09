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
        .header { padding: 10px; background: #111; border-bottom: 3px solid #00ff88; text-align: center; }
        .ia-console { background: #000; border: 2px solid #00ff88; border-radius: 12px; padding: 15px; width: 90%; margin: 10px auto; }
        #ia-orden { width: 70%; padding: 12px; background: #111; color: #00ff88; border: 1px solid #333; border-radius: 5px; font-size: 16px; outline: none;}
        .btn-enviar { padding: 12px 25px; background: #00ff88; color: black; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; transition: 0.3s; }
        .btn-enviar:hover { background: #6a00ff; color: white; }
        
        #piano-container { display: flex; justify-content: center; padding: 20px; background: #000; overflow-x: auto; }
        #piano { display: flex; height: 220px; position: relative; }
        .key-white { width: 40px; height: 100%; border: 1px solid #222; background: white; border-radius: 0 0 5px 5px; position: relative; cursor: pointer; transition: 0.1s;}
        .key-black { width: 26px; height: 130px; background: #222; margin-left: -13px; margin-right: -13px; z-index: 2; border-radius: 0 0 3px 3px; cursor: pointer; transition: 0.1s;}
        
        .ia-touch { background: #00ff88 !important; box-shadow: 0 0 35px #00ff88 !important; transform: translateY(5px); }
        .note-label { position: absolute; bottom: 5px; width: 100%; text-align: center; color: #888; font-size: 9px; font-weight: bold; pointer-events: none; }
    </style>
</head>
<body>

<div class="header">
    <h2 style="margin:0;">🎹 KORYM AI: SONIDO TOTAL</h2>
    <div class="ia-console">
        <input type="text" id="ia-orden" placeholder="Ej: 'Toca C4', 'Acorde de Em', 'Escala Mayor'...">
        <button class="btn-enviar" onclick="ejecutarOrden()">COMANDAR</button>
        <div id="feedback-ia" style="margin-top:10px; color:#00ff88; font-family:monospace;">IA: Haz clic en cualquier tecla para activar el sonido.</div>
    </div>
</div>

<div id="piano-container"><div id="piano"></div></div>

<script>
    // 1. MOTOR DE SONIDO (Polifónico para acordes)
    const synth = new Tone.PolySynth(Tone.Synth, {
        oscillator: { type: "triangle" },
        envelope: { attack: 0.05, release: 1 }
    }).toDestination();

    // 2. GENERACIÓN DE TECLADO (4 Octavas: de C2 a B5)
    const notesBase = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    let keysElements = [];
    const pianoDiv = document.getElementById('piano');

    for (let i = 0; i < 48; i++) {
        let name = notesBase[i % 12];
        let octave = Math.floor(i / 12) + 2;
        let fullNote = name + octave;
        let isBlack = name.includes("#");
        
        const div = document.createElement('div');
        div.className = isBlack ? "key-black" : "key-white";
        div.innerHTML = `<span class="note-label">${fullNote}</span>`;
        
        // Tocar al hacer click manual
        div.onmousedown = () => { 
            Tone.start();
            synth.triggerAttack(fullNote); 
            div.classList.add('ia-touch');
        };
        div.onmouseup = () => { 
            synth.triggerRelease(fullNote); 
            div.classList.remove('ia-touch');
        };

        pianoDiv.appendChild(div);
        keysElements.push({ el: div, name: name, full: fullNote, noteIndex: i % 12 });
    }

    const ACORDES = {
        "m": [0, 3, 7], "maj": [0, 4, 7], "7": [0, 4, 7, 10], "m7": [0, 3, 7, 10],
        "maj7": [0, 4, 7, 11], "dim": [0, 3, 6], "aug": [0, 4, 8], "sus4": [0, 5, 7]
    };

    // 3. MOTOR DE RECONOCIMIENTO Y EJECUCIÓN (Visual + Audio)
    async function ejecutarOrden() {
        await Tone.start();
        const rawCmd = document.getElementById('ia-orden').value.toUpperCase();
        const cmd = rawCmd.replace("ACORDE DE ", "").replace("TOCA ", "").trim();
        const fb = document.getElementById('feedback-ia');
        
        // Limpiar estado anterior
        keysElements.forEach(k => k.el.classList.remove('ia-touch'));

        // Caso 1: Nota Simple (Ej: "C4")
        let notaSimple = keysElements.find(k => k.full === cmd || k.name === cmd);
        if (notaSimple) {
            notaSimple.el.classList.add('ia-touch');
            synth.triggerAttackRelease(notaSimple.full, "2n");
            fb.innerText = "IA: Tocando nota " + notaSimple.full;
            setTimeout(() => notaSimple.el.classList.remove('ia-touch'), 500);
            return;
        }

        // Caso 2: Acordes Universales
        let raiz = "";
        let tipo = "maj";

        if (cmd[1] === "#" || cmd[1] === "B") { raiz = cmd.substring(0, 2); tipo = cmd.substring(2) || "maj"; }
        else { raiz = cmd[0]; tipo = cmd.substring(1) || "maj"; }
        if (tipo === "M") tipo = "maj";

        let rootIndex = notesBase.indexOf(raiz);
        if (rootIndex !== -1) {
            let intervalos = ACORDES[tipo.toLowerCase()] || ACORDES["maj"];
            let notasParaTocar = [];

            // Buscar las notas en la octava central (Octava 4)
            keysElements.forEach(k => {
                intervalos.forEach(inter => {
                    if (k.noteIndex === (rootIndex + inter) % 12 && k.full.includes("4")) {
                        k.el.classList.add('ia-touch');
                        notasParaTocar.push(k.full);
                    }
                });
            });

            if (notasParaTocar.length > 0) {
                synth.triggerAttackRelease(notasParaTocar, "2n");
                fb.innerText = "IA: Ejecutando acorde " + raiz + " " + tipo;
                setTimeout(() => keysElements.forEach(k => k.el.classList.remove('ia-touch')), 1000);
            }
        } else {
            fb.innerText = "IA: No reconozco esa instrucción musical.";
        }
    }
</script>
</body>
</html>
"""

components.html(piano_ia_html, height=650, scrolling=False)
