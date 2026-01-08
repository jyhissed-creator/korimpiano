import streamlit as st
import streamlit.components.v1 as components

# 1. ESTILO OPTIMIZADO PARA MÓVIL
st.set_page_config(page_title="KORYMpiano Smart Tutor", layout="wide")
st.markdown("""
<style>
    .creadora { text-align: center; color: #6a1b9a; font-weight: bold; font-size: 1.8em; margin-bottom: 10px; }
    .status-box { background: #ffffff; border-radius: 10px; padding: 15px; border: 2px solid #6a1b9a; text-align: center; font-size: 0.9em; }
    /* CONTENEDOR DEL PIANO PARA CELULAR */
    .piano-scroll { overflow-x: auto; background: #222; padding: 10px; border-radius: 10px; display: flex; justify-content: flex-start; }
    .piano-container { display: flex; position: relative; height: 160px; min-width: 600px; margin: 0 auto; }
    .key { border: 1px solid #000; text-align: center; font-weight: bold; transition: 0.1s; user-select: none; position: relative; }
    .white { width: 50px; height: 150px; background: white; color: #333; z-index: 1; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 5px; }
    .black { width: 34px; height: 90px; background: black; color: white; margin-left: -17px; margin-right: -17px; z-index: 2; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 5px; font-size: 0.8em; }
    /* COLORES DE GUÍA Y BLUETOOTH */
    .guia-der { background-color: #c8e6c9 !important; border-bottom: 8px solid #4caf50; } 
    .pressed { background-color: #ffeb3b !important; box-shadow: inset 0 0 15px #fbc02d; } 
    .match { background-color: #ff5722 !important; color: white !important; } 
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='creadora'>🎹 KORYMpiano: Tutor Inteligente</div>", unsafe_allow_html=True)

# 2. MOTOR DE TRANSPORTE Y ACORDES
NOTAS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
ACORDES_MAP = {
    'C': [0, 4, 7], 'Cm': [0, 3, 7], 'C#': [1, 5, 8], 'D': [2, 6, 9], 'Dm': [2, 5, 9],
    'Eb': [3, 7, 10], 'E': [4, 8, 11], 'Em': [4, 7, 11], 'F': [5, 9, 0], 'F#': [6, 10, 1],
    'G': [7, 11, 2], 'Gm': [7, 10, 2], 'Ab': [8, 0, 3], 'A': [9, 1, 4], 'Am': [9, 0, 4],
    'Bb': [10, 2, 5], 'B': [11, 3, 6], 'C#m': [1, 4, 8], 'F#m': [6, 9, 1], 'G#m': [8, 11, 3], 'A#m': [10, 1, 5], 'D#m': [3, 6, 10]
}

def transportar(acorde, origen, destino):
    es_m = "m" in acorde
    base = acorde.replace("m", "")
    if base not in NOTAS: return acorde
    dif = NOTAS.index(destino) - NOTAS.index(origen)
    nueva_pos = (NOTAS.index(base) + dif) % 12
    return NOTAS[nueva_pos] + ("m" if es_m else "")

# 3. INTERFAZ LATERAL
st.sidebar.header("🎯 CONFIGURACIÓN")
video_url = st.sidebar.text_input("YouTube URL:", "https://youtu.be/Xyuuv5co7ko")
letra = st.sidebar.text_area("Letra y Acordes:", "F Bb C Am Dm Gm")
tono_original = st.sidebar.selectbox("Tono Original:", NOTAS, index=5) # F
tono_deseado = st.sidebar.selectbox("Tono para Practicar:", NOTAS, index=6) # F#

# 4. VIDEO
st.video(video_url)
acordes_detectados = list(dict.fromkeys([w for w in letra.split() if any(n in w for n in NOTAS)]))

if 'target' not in st.session_state: st.session_state.target = []

# 5. PIANO INTERACTIVO (CORREGIDO PARA VERSE COMO PIANO)
def render_piano(objetivos):
    obj_js = ",".join(objetivos)
    teclas_html = ""
    for n in NOTAS:
        clase = "black" if "#" in n else "white"
        guia = "guia-der" if n in objetivos else ""
        teclas_html += f'<div class="key {clase} {guia}" id="k-{n}">{n}</div>'

    html_code = f"""
    <div id="msg" style="color:#6a1b9a; font-weight:bold; text-align:center; margin-bottom:5px;">🎹 Conecta tu Piano Bluetooth</div>
    <div class="piano-scroll">
        <div class="piano-container">{teclas_html}</div>
    </div>
    <script>
    const objetivos = "{obj_js}".split(",");
    if (navigator.requestMIDIAccess) {{
        navigator.requestMIDIAccess({{ bluetooth: true }}).then(midi => {{
            for (let input of midi.inputs.values()) {{
                input.onmidimessage = (m) => {{
                    const [s, n, v] = m.data;
                    const nota = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][n % 12];
                    const el = document.getElementById('k-' + nota);
                    if (s === 144 && v > 0) {{
                        el.classList.add('pressed');
                        if (objetivos.includes(nota)) el.classList.add('match');
                    }} else if (s === 128 || (s === 144 && v === 0)) {{
                        el.classList.remove('pressed');
                        el.classList.remove('match');
                    }}
                }};
            }}
        }});
    }}
    </script>
    """
    components.html(html_code, height=220)

# 6. BOTONES DE ACORDES
st.subheader(f"🎶 Tonalidad: {tono_deseado}")
cols = st.columns(4)
for i, ac in enumerate(acordes_detectados):
    ac_t = transportar(ac, tono_original, tono_deseado)
    with cols[i % 4]:
        if st.button(ac_t, key=f"btn_{i}", use_container_width=True):
            base = ac_t.replace("m", "")
            intervalos = ACORDES_MAP.get(ac_t, [0,4,7])
            st.session_state.target = [NOTAS[(NOTAS.index(base) + s) % 12] for s in intervalos]

render_piano(st.session_state.target)

# 7. EXPLICACIÓN
if st.session_state.target:
    st.markdown(f"""
    <div class='status-box'>
        <b>Mano Izquierda (Bajo):</b> Toca {st.session_state.target[0]}<br>
        <b>Mano Derecha (Acorde):</b> Toca juntas {", ".join(st.session_state.target)}
    </div>
    """, unsafe_allow_html=True)
    
