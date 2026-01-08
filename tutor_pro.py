import streamlit as st
import streamlit.components.v1 as components

# 1. ESTILO DE ALTA FIDELIDAD (Basado en tu dibujo)
st.set_page_config(page_title="KORYMpiano Pro", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    /* Fondo oscuro profesional */
    .main { background-color: #0e1117; }
    
    /* Contenedor Superior: Letra y Video lado a lado */
    .dashboard {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        margin-bottom: 20px;
    }
    
    .lyrics-panel {
        flex: 1;
        min-width: 300px;
        background: #1c1f26;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #9c27b0;
        height: 350px;
        overflow-y: auto;
        color: #e0e0e0;
        font-family: 'Courier New', Courier, monospace;
        white-space: pre-wrap;
    }

    .video-panel {
        flex: 1.5;
        min-width: 300px;
    }

    /* EL PIANO MAESTRO (Ocupa todo el ancho abajo) */
    .piano-section {
        background: #000;
        padding: 30px 10px;
        border-radius: 20px;
        border: 1px solid #333;
        margin-top: 20px;
    }

    .piano-container {
        overflow-x: auto;
        display: flex;
        justify-content: center;
    }

    .keyboard {
        position: relative;
        width: 850px;
        height: 250px;
        background: #111;
    }

    .key {
        position: absolute;
        border: 1px solid #555;
        border-radius: 0 0 8px 8px;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        transition: 0.1s;
        font-weight: bold;
        padding-bottom: 15px;
        user-select: none;
    }

    .white { width: 60px; height: 240px; background: white; z-index: 1; color: #999; }
    .black { width: 38px; height: 140px; background: #222; z-index: 2; color: #fff; font-size: 10px; }

    /* COLORES DE MANO DE TU DIBUJO */
    .izq-verde { background-color: #4CAF50 !important; color: white !important; box-shadow: inset 0 -15px 0 #2E7D32; }
    .der-azul { background-color: #2196F3 !important; color: white !important; box-shadow: inset 0 -15px 0 #1565C0; }
</style>
""", unsafe_allow_html=True)

# 2. LÓGICA MUSICAL
NOTAS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
ACORDES_MAP = {
    'C': [0, 4, 7], 'G': [7, 11, 2], 'Am': [9, 0, 4], 'F': [5, 9, 0], 
    'F#': [6, 10, 1], 'C#': [1, 5, 8], 'Bb': [10, 2, 5], 'Dm': [2, 5, 9]
}

# 3. BARRA LATERAL (Solo para ajustes técnicos)
with st.sidebar:
    st.title("🎹 Configuración")
    url = st.text_input("YouTube URL", "https://youtu.be/Xyuuv5co7ko")
    letra_raw = st.text_area("Letra y Acordes", "Coro:\nF  Bb  C\nGracias Señor quiero darte")
    tono_actual = st.selectbox("Tono Original", NOTAS, index=5) # F
    tono_deseado = st.selectbox("Transportar a", NOTAS, index=5)

dif = NOTAS.index(tono_deseado) - NOTAS.index(tono_actual)

# 4. CUERPO DE LA APP (EL DISEÑO DE TU IMAGEN)
st.markdown("<h2 style='text-align:center; color:white;'>KORYMpiano Maestro</h2>", unsafe_allow_html=True)

# Fila 1: Letra y Video
st.markdown('<div class="dashboard">', unsafe_allow_html=True)
col_l, col_v = st.columns([1, 1.5])

with col_l:
    st.markdown(f'<div class="lyrics-panel">{letra_raw}</div>', unsafe_allow_html=True)

with col_v:
    st.video(url)
st.markdown('</div>', unsafe_allow_html=True)

# Fila 2: Botones de Acordes (Grandes para dedos)
acordes = [a for a in letra_raw.split() if any(n in a for n in NOTAS)]
if 'selected_chord' not in st.session_state: st.session_state.selected_chord = []

st.write("### 🖐️ Selecciona el acorde para ver la posición:")
c_btns = st.columns(len(set(acordes)))
for i, ac in enumerate(sorted(list(set(acordes)))):
    base = ac.replace("m", "")
    nueva_pos = (NOTAS.index(base) + dif) % 12
    notas_finales = [NOTAS[(nueva_pos + i) % 12] for i in ([0,3,7] if "m" in ac else [0,4,7])]
    
    if c_btns[i].button(ac if dif == 0 else NOTAS[nueva_pos] + ("m" if "m" in ac else "")):
        st.session_state.selected_chord = notas_finales

# Fila 3: El Piano Maestro
# Definimos las posiciones exactas para 2 octavas
p_pos = {'C':0, 'C#':40, 'D':60, 'D#':105, 'E':120, 'F':180, 'F#':220, 'G':240, 'G#':285, 'A':300, 'A#':345, 'B':360}

teclas_render = ""
for oct in [0, 420]:
    for n in NOTAS:
        tipo = "black" if "#" in n else "white"
        clase_mano = ""
        if n in st.session_state.selected_chord:
            clase_mano = "izq-verde" if n == st.session_state.selected_chord[0] else "der-azul"
        
        teclas_render += f'<div class="key {tipo} {clase_mano}" style="left:{p_pos[n]+oct}px">{n}</div>'

html_piano = f"""
<div class="piano-section">
    <div class="piano-container">
        <div class="keyboard">{teclas_render}</div>
    </div>
</div>
<div style="text-align:center; margin-top:10px; color:#aaa;">
    🟢 Mano Izquierda (Bajo) | 🔵 Mano Derecha (Acorde)
</div>
"""
components.html(html_piano, height=350)
