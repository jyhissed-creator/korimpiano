import streamlit as st
import streamlit.components.v1 as components
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="KORYMpiano", page_icon="🎹", layout="centered")

# --- MOTOR DE DATOS ---
NOTAS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
ENARMONIAS = {
    'DB': 'C#', 'EB': 'D#', 'GB': 'F#', 'AB': 'G#', 'BB': 'A#',
    'REB': 'C#', 'MIB': 'D#', 'SOLB': 'F#', 'LAB': 'G#', 'SIB': 'A#',
    'B#': 'C', 'E#': 'F', 'FB': 'E', 'CB': 'B'
}

INTERVALOS = {
    "": [0, 4, 7], "m": [0, 3, 7], "7": [0, 4, 7, 10], "maj7": [0, 4, 7, 11],
    "m7": [0, 3, 7, 10], "9": [0, 4, 7, 10, 14], "maj9": [0, 4, 7, 11, 14],
    "m9": [0, 3, 7, 10, 14], "11": [0, 4, 7, 10, 14, 17], "13": [0, 4, 7, 10, 14, 17, 21],
    "dim": [0, 3, 6], "dim7": [0, 3, 6, 9], "aug": [0, 4, 8], "sus4": [0, 5, 7], 
    "sus2": [0, 2, 7], "add9": [0, 4, 7, 14], "m7b5": [0, 3, 6, 10], "7b9": [0, 4, 7, 10, 13]
}

def normalizar(n):
    n = n.upper()
    return ENARMONIAS.get(n, n)

def generar_audio_acorde(notas):
    notas_audio = [f"{n}4" for n in notas]
    notas_js = str(notas_audio)

    js_code = f"""
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>
    <button id="play-btn" style="
        background-color: #2E7D32; color: white; border: none; 
        padding: 12px 24px; border-radius: 8px; cursor: pointer;
        font-weight: bold; font-size: 16px; width: 100%; margin-top: 10px;">
        🔊 Escuchar Sonido Real
    </button>
    <script>
        const synth = new Tone.PolySynth(Tone.Synth).toDestination();
        document.getElementById('play-btn').addEventListener('click', async () => {{
            await Tone.start();
            synth.triggerAttackRelease({notas_js}, "1.5n");
        }});
    </script>
    """
    components.html(js_code, height=80)

# --- INTERFAZ PRINCIPAL ---
st.title("🎹 KORYMpiano")
st.markdown("### El Motor Lógico de Acordes")
st.write("Escribe un acorde para ver cómo se toca y cómo suena.")

entrada_usuario = st.text_input("Introduce un acorde (ej: Cmaj7, Am/G, F#9):").strip()

if entrada_usuario:
    partes = entrada_usuario.split('/')
    cifrado = partes[0]
    bajo_manual = normalizar(partes[1]) if len(partes) > 1 else None

    match = re.match(r"^([a-gA-G][#b]?)(.*)$", cifrado)
    
    if match:
        raiz = normalizar(match.group(1))
        tipo = match.group(2)
        
        if raiz in NOTAS:
            idx_raiz = NOTAS.index(raiz)
            ints = INTERVALOS.get(tipo, [0, 4, 7])
            notas_acorde = [NOTAS[(idx_raiz + i) % 12] for i in ints]
            bajo_final = bajo_manual if bajo_manual else notas_acorde[0]

            st.success(f"Análisis de **{entrada_usuario.upper()}**")
            
            generar_audio_acorde(notas_acorde)
            
            col1, col2 = st.columns(2)
            with col1:
                st.info("🫲 Mano Izquierda")
                st.subheader(f"Bajo: {bajo_final}")
            with col2:
                st.info("🫱 Mano Derecha")
                for i, n in enumerate(notas_acorde):
                    if n == bajo_final and i == 0: continue
                    st.write(f"**{n}**")

            st.markdown("#### Teclado Virtual")
            teclas_html = "<div style='background-color: #222; padding: 20px; border-radius: 10px; text-align: center;'>"
            for n in NOTAS:
                color = "#4CAF50" if n in notas_acorde else "white"
                txt_color = "white" if n in notas_acorde else "black"
                teclas_html += f"<div style='display:inline-block; width:35px; height:100px; background-color:{color}; border:1px solid #333; color:{txt_color}; font-weight:bold; margin:1px;'>{n}</div>"
            teclas_html += "</div>"
            st.markdown(teclas_html, unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("KORYM Tech")
st.sidebar.write("### 👤 Creadora")
st.sidebar.info("Desarrollado por **Yhissed Jiménez**.")
st.sidebar.write("© 2024 KORYMpiano")
