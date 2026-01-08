import streamlit as st
import streamlit.components.v1 as components

# 1. ESTILO Y CONFIGURACIÓN
st.set_page_config(page_title="KORYMpiano Smart Tutor", layout="wide")
st.markdown("""
<style>
    .creadora { text-align: center; color: #6a1b9a; font-weight: bold; font-size: 2.2em; }
    .status-box { background: #ffffff; border-radius: 15px; padding: 20px; border: 2px solid #6a1b9a; text-align: center; }
    .piano-container { display: flex; justify-content: center; background: #222; padding: 20px; border-radius: 10px; }
    .key { border: 1px solid #000; text-align: center; line-height: 180px; font-weight: bold; transition: 0.1s; font-size: 10px; }
    .white { width: 50px; height: 180px; background: white; color: #333; }
    .black { width: 30px; height: 110px; background: black; color: white; margin-left: -15px; margin-right: -15px; z-index: 2; }
    /* COLORES DE FEEDBACK */
    .guia-izq { background-color: #bbdefb !important; border: 3px solid #2196f3; } /* Lo que DEBES tocar (Izq) */
    .guia-der { background-color: #c8e6c9 !important; border: 3px solid #4caf50; } /* Lo que DEBES tocar (Der) */
    .pressed { background-color: #ffeb3b !important; box-shadow: 0 0 20px #fbc02d; } /* Lo que ESTÁS tocando tú */
    .match { background-color: #ff5722 !important; box-shadow: 0 0 25px #ff5722; } /* ¡ACIERTO! */
</style>
""", unsafe_allow_html=True)

# 2. LÓGICA MUSICAL Y TRANSPORTE
NOTAS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
ACORDES_MAP = {
    'C': [0, 4, 7], 'Cm': [0, 3, 7], 'C#': [1, 5, 8], 'D': [2, 6, 9], 'Dm': [2, 5, 9],
    'Eb': [3, 7, 10], 'E': [4, 8, 11], 'Em': [4, 7, 11], 'F': [5, 9, 0], 'F#': [6, 10, 1],
    'G': [7, 11, 2], 'Gm': [7, 10, 2], 'Ab': [8, 0, 3], 'A': [9, 1, 4], 'Am': [9, 0, 4],
    'Bb': [10, 2, 5], 'B': [11, 3, 6]
}

def transportar(acorde, origen, destino):
    es_m = "m" in acorde
    base = acorde.replace("m", "")
    if base not in NOTAS: return acorde
    dif = NOTAS.index(destino) - NOTAS.index(origen)
    nueva_pos = (NOTAS.index(base) + dif) % 12
    return NOTAS[nueva_pos] + ("m" if es_m else "")

# 3. INTERFAZ LATERAL
st.sidebar.header("🎹 KORYM TECH SETTINGS")
video_url = st.sidebar.text_input("YouTube URL:", "https://youtu.be/Xyuuv5co7ko")
letra = st.sidebar.text_area("Letra y Acordes:", "F Bb C Am")
tono_original = st.sidebar.selectbox("Tono Original de la letra:", NOTAS, index=5)
tono_deseado = st.sidebar.selectbox("Tono para practicar:", NOTAS, index=6)

# 4. PROCESAMIENTO
st.video(video_url)
acordes_raw = list(set([w for w in letra.split() if any(n in w for n in NOTAS)]))

if 'target_notas' not in st.session_state: st.session_state.target_notas = []

# 5. PIANO VIRTUAL CON BLUETOOTH MIDI INTEGRADO
def tutor_interactivo(objetivos):
    # Convertimos la lista de notas objetivo a un string para JavaScript
    obj_js = ",".join(objetivos)
    
    html_code = f"""
    <div id="feedback-midi" style="text-align:center; font-weight:bold; color:#6a1b9a; margin-bottom:10px;">
        ⚠️ Piano Bluetooth no detectado. Conéctalo para evaluar tu ritmo.
    </div>
    <div class="piano-container">
        {"".join([f'<div class="key {"black" if "#" in n else "white"} {"guia-der" if n in objetivos else ""}" id="k-{n}">{n}</div>' for n in NOTAS])}
    </div>

    <script>
    const objetivos = "{obj_js}".split(",");
    const feedback = document.getElementById('feedback-midi');
    
    if (navigator.requestMIDIAccess) {{
        navigator.requestMIDIAccess({{ bluetooth: true }}).then(access => {{
            feedback.innerText = "✅ PIANO CONECTADO. ¡Sigue las teclas verdes!";
            for (let input of access.inputs.values()) {{
                input.onmidimessage = (msg) => {{
                    const [status, note, velocity] = msg.data;
                    const notaNombre = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][note % 12];
                    const el = document.getElementById('k-' + notaNombre);
                    
                    if (status === 144 && velocity > 0) {{
                        el.classList.add('pressed');
                        if (objetivos.includes(notaNombre)) {{
                            el.classList.add('match');
                            feedback.innerText = "⭐ ¡EXCELENTE! Nota correcta y a tiempo.";
                        }} else {{
                            feedback.innerText = "❌ Esa nota no va en este acorde. Intenta otra vez.";
                        }}
                    }} else if (status === 128 || (status === 144 && velocity === 0)) {{
                        el.classList.remove('pressed');
                        el.classList.remove('match');
                    }}
                }};
            }}
        }});
    }}
    </script>
    """
    components.html(html_code, height=300)

# 6. BOTONES DE ACORDES TRANSPORTADOS
st.subheader(f"🎼 Tonalidad Actual: {tono_deseado}")
cols = st.columns(len(acordes_raw) if acordes_raw else 1)
for i, ac in enumerate(acordes_raw):
    ac_t = transportar(ac, tono_original, tono_deseado)
    if cols[i % len(cols)].button(ac_t):
        base = ac_t.replace("m", "")
        intervalos = ACORDES_MAP.get(ac_t, [0,4,7])
        st.session_state.target_notas = [NOTAS[(NOTAS.index(base) + s) % 12] for s in intervalos]

tutor_interactivo(st.session_state.target_notas)

st.markdown("""
<div class='status-box'>
    <b>¿Cómo practicar?</b><br>
    1. Elige un acorde. Se pondrá <b>Verde</b> en el piano virtual.<br>
    2. Toca tu piano real. Verás una luz <b>Amarilla</b> donde presionas.<br>
    3. Si logras que la luz sea <b>Naranja</b>, significa que diste en el blanco.
</div>
""", unsafe_allow_html=True)
