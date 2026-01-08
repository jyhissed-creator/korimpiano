import streamlit as st
import streamlit.components.v1 as components

# 1. CSS AVANZADO: POSICIONAMIENTO REAL DE TECLAS
st.set_page_config(page_title="KORYMpiano Virtual", layout="wide")
st.markdown("""
<style>
    .creadora { text-align: center; color: #6a1b9a; font-weight: bold; font-size: 1.5em; }
    
    /* El contenedor que permite deslizar el piano en el celular */
    .piano-scroll {
        overflow-x: auto;
        padding: 20px 10px;
        background: #1a1a1a;
        border-radius: 15px;
        width: 100%;
    }

    /* Contenedor del piano con tamaño fijo para que no se deforme */
    .piano-board {
        position: relative;
        width: 500px; /* Ancho total del piano */
        height: 180px;
        margin: 0 auto;
        background: #1a1a1a;
    }

    .key {
        position: absolute;
        cursor: pointer;
        border: 1px solid #000;
        border-radius: 0 0 5px 5px;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        font-weight: bold;
        transition: 0.1s;
        user-select: none;
    }

    /* Teclas Blancas */
    .white {
        width: 71px; /* 500 / 7 notas blancas aprox */
        height: 170px;
        background: white;
        color: #333;
        z-index: 1;
        font-size: 12px;
        padding-bottom: 10px;
    }

    /* Teclas Negras (Posicionadas encima) */
    .black {
        width: 40px;
        height: 100px;
        background: black;
        color: white;
        z-index: 2;
        font-size: 10px;
        padding-bottom: 5px;
    }

    /* Colores de guía y presión */
    .active-guide { background-color: #c8e6c9 !important; border-bottom: 8px solid #4caf50; }
    .midi-pressed { background-color: #ffeb3b !important; transform: translateY(3px); }
    .perfect { background-color: #ff5722 !important; color: white !important; }

    /* Botones de acordes estilo cuadrícula móvil */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        background: white;
        border: 2px solid #6a1b9a;
        color: #6a1b9a;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 2. LÓGICA DE TRANSPORTE
NOTAS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
MODELO = {'MAYOR': [0, 4, 7], 'MENOR': [0, 3, 7]}

def generar_acorde(texto, semitonos):
    es_m = "m" in texto
    base = texto.replace("m", "").strip()
    if base not in NOTAS: return None
    pos = (NOTAS.index(base) + semitonos) % 12
    notas = [NOTAS[(pos + i) % 12] for i in MODELO['MENOR' if es_m else 'MAYOR']]
    return {"nombre": NOTAS[pos] + ("m" if es_m else ""), "notas": notas}

# 3. INTERFAZ
st.markdown("<div class='creadora'>🎹 KORYMpiano Virtual</div>", unsafe_allow_html=True)

with st.sidebar:
    url = st.text_input("YouTube URL", "https://youtu.be/Xyuuv5co7ko")
    acordes_input = st.text_area("Acordes", "F# B C# A#m D#m G#m")
    t_orig = st.selectbox("Tono Original", NOTAS, index=6)
    t_dest = st.selectbox("Transportar a", NOTAS, index=0)

dif = NOTAS.index(t_dest) - NOTAS.index(t_orig)
st.video(url)

if 'notas_obj' not in st.session_state: st.session_state.notas_obj = []

# Botones de acordes
lista = acordes_input.split()
for i in range(0, len(lista), 3):
    cols = st.columns(3)
    for j, ac in enumerate(lista[i:i+3]):
        info = generar_acorde(ac, dif)
        if info and cols[j].button(info['nombre'], key=f"b{i+j}"):
            st.session_state.notas_obj = info['notas']

# 4. EL PIANO VIRTUAL (HTML + JS)
# Definimos posiciones exactas para que parezca un piano
posiciones = {
    'C': 'left:0px', 'C#': 'left:50px', 'D': 'left:71px', 'D#': 'left:125px',
    'E': 'left:142px', 'F': 'left:213px', 'F#': 'left:265px', 'G': 'left:284px',
    'G#': 'left:340px', 'A': 'left:355px', 'A#': 'left:415px', 'B': 'left:426px'
}

teclas_html = ""
for n in NOTAS:
    tipo = "black" if "#" in n else "white"
    guia = "active-guide" if n in st.session_state.notas_obj else ""
    teclas_html += f'<div class="key {tipo} {guia}" id="key-{n}" style="{posiciones[n]}">{n}</div>'

html_piano = f"""
<script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>
<div id="status" style="text-align:center; color:white; background:#6a1b9a; padding:10px; border-radius:10px; margin-bottom:10px; cursor:pointer; font-family:sans-serif;">
    👉 TOCA AQUÍ PARA ACTIVAR SONIDO Y MIDI 👈
</div>
<div class="piano-scroll">
    <div class="piano-board">{teclas_html}</div>
</div>
<script>
const synth = new Tone.PolySynth(Tone.Synth).toDestination();
const objetivos = "{",".join(st.session_state.notas_obj)}".split(",");
const status = document.getElementById('status');

status.addEventListener('click', async () => {{
    await Tone.start();
    status.innerText = "🎹 PIANO VIRTUAL LISTO";
}});

if (navigator.requestMIDIAccess) {{
    navigator.requestMIDIAccess({{ bluetooth: true }}).then(midi => {{
        for (let input of midi.inputs.values()) {{
            input.onmidimessage = (m) => {{
                const [cmd, note, vel] = m.data;
                const nNombre = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][note % 12];
                const el = document.getElementById('key-' + nNombre);
                if (cmd === 144 && vel > 0) {{
                    synth.triggerAttack(nNombre + "4");
                    if(el) el.classList.add('midi-pressed');
                    if (objetivos.includes(nNombre)) el.classList.add('perfect');
                }} else if (cmd === 128 || (cmd === 144 && vel === 0)) {{
                    synth.triggerRelease(nNombre + "4");
                    if(el) {{ el.classList.remove('midi-pressed'); el.classList.remove('perfect'); }}
                }}
            }};
        }}
    }});
}}
</script>
"""
components.html(html_piano, height=300)
