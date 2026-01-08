Import streamlit as st
import streamlit.components.v1 as components

# ================================
# 1. ESTILO Y MARCA (KORYM TECH)
# ================================

st.set_page_config(page_title="KORYMpiano Tutor", layout="wide")

st.markdown("""
<style>
    .creadora { text-align: center; color: #6a1b9a; font-weight: bold; font-size: 2.2em; margin-bottom: 20px; }
    .status-box { background: #f3e5f5; border-radius: 15px; padding: 20px; border-top: 5px solid #6a1b9a; margin-top: 20px; }
    .piano-container { display: flex; justify-content: center; background: #222; padding: 20px; border-radius: 10px; }
    .key { border: 1px solid #000; text-align: center; line-height: 200px; font-weight: bold; transition: 0.2s; user-select: none; font-size: 12px; }
    .white { width: 50px; height: 180px; background: white; color: #333; }
    .black { width: 30px; height: 110px; background: black; color: white; margin-left: -15px; margin-right: -15px; z-index: 2; }
    /* Colores de Guía Visual */
    .guia-izq { background-color: #bbdefb !important; box-shadow: 0 0 20px #2196f3; color: transparent; }
    .guia-der { background-color: #c8e6c9 !important; box-shadow: 0 0 20px #4caf50; color: transparent; }
    .correct { background-color: #ffeb3b !important; box-shadow: 0 0 20px #fbc02d; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='creadora'>🎹 KORYMpiano: Tutor Visual Inteligente</div>", unsafe_allow_html=True)

# ================================
# 2. LÓGICA MUSICAL
# ================================

# Acordes con notas de triada
ACORDES_DATA = {
    'F#': ['F#', 'A#', 'C#'], 'B': ['B', 'D#', 'F#'], 'C#': ['C#', 'F', 'G#'],
    'A#m': ['A#', 'C#', 'F'], 'D#m': ['D#', 'F#', 'A#'], 'G#m': ['G#', 'B', 'D#'],
    'F': ['F', 'A', 'C'], 'Bb': ['A#', 'D', 'F'], 'C': ['C', 'E', 'G'],
    'Am': ['A', 'C', 'E'], 'Dm': ['D', 'F', 'A'], 'Gm': ['G', 'A#', 'D']
}

# ================================
# 3. BARRA LATERAL
# ================================

st.sidebar.header("🎓 CONFIGURACIÓN")
video_url = st.sidebar.text_input("YouTube URL:", "https://youtu.be/Xyuuv5co7ko")
acordes_raw = st.sidebar.text_area("Acordes de la canción (separados por espacio):", "F# B C# A#m D#m G#m")

# ================================
# 4. VIDEO
# ================================
st.video(video_url)

# ================================
# 5. TECLADO VIRTUAL INTERACTIVO
# ================================

if 'teclas_izq' not in st.session_state:
    st.session_state.teclas_izq = []
if 'teclas_der' not in st.session_state:
    st.session_state.teclas_der = []

def mostrar_piano(izq, der):
    def clase_guia(n):
        if n in izq:
            return "guia-izq"
        elif n in der:
            return "guia-der"
        else:
            return ""
    
    html_piano = f"""
    <div class="piano-container">
        <div class="key white {clase_guia('C')}" id="C">C</div> <div class="key black {clase_guia('C#')}" id="C#">C#</div>
        <div class="key white {clase_guia('D')}" id="D">D</div> <div class="key black {clase_guia('D#')}" id="D#">D#</div>
        <div class="key white {clase_guia('E')}" id="E">E</div>
        <div class="key white {clase_guia('F')}" id="F">F</div> <div class="key black {clase_guia('F#')}" id="F#">F#</div>
        <div class="key white {clase_guia('G')}" id="G">G</div> <div class="key black {clase_guia('G#')}" id="G#">G#</div>
        <div class="key white {clase_guia('A')}" id="A">A</div> <div class="key black {clase_guia('A#')}" id="A#">A#</div>
        <div class="key white {clase_guia('B')}" id="B">B</div>
    </div>
    <script>
    navigator.requestMIDIAccess({{ bluetooth: true }}).then(access => {{
        for (let input of access.inputs.values()) {{
            input.onmidimessage = (msg) => {{
                const [s, n, v] = msg.data;
                const notas = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
                const tecla = document.getElementById(notas[n % 12]);
                if (s === 144 && v > 0) tecla.classList.add('correct');
                else tecla.classList.remove('correct');
            }};
        }}
    }});
    </script>
    """
    components.html(html_piano, height=230)

# ================================
# 6. BOTONES DE ACORDES
# ================================

st.markdown("### 🎶 Toca el acorde para ver cómo se hace:")
lista_ac = acordes_raw.split()
cols = st.columns(len(lista_ac))

for i, ac in enumerate(lista_ac):
    if cols[i].button(ac, key=f"btn_{i}"):
        notas = ACORDES_DATA.get(ac, [])
        if notas:
            st.session_state.teclas_izq = [notas[0]]       # mano izquierda toca la raíz
            st.session_state.teclas_der = notas             # mano derecha toca todo el acorde

mostrar_piano(st.session_state.teclas_izq, st.session_state.teclas_der)

# ================================
# 7. EXPLICACIÓN POR MANO
# ================================

def explicacion_manos(acorde):
    notas = ACORDES_DATA.get(acorde, [])
    if not notas:
        return "No hay información para este acorde."
    mano_izq = notas[0]
    mano_der = " - ".join(notas)
    texto = f"""
    👩‍🏫 **Cómo tocar {acorde}:**  
    - **Mano izquierda (Bajo):** toca la nota **{mano_izq}**, marcando el pulso (1,2,3,4).  
    - **Mano derecha (Acorde):** toca estas notas juntas: **{mano_der}**.  
    - **Ritmo sugerido:** izquierda en el primer tiempo, derecha en los 4 tiempos, o arpegio si quieres.
    """
    return texto

st.markdown("<div class='status-box'>", unsafe_allow_html=True)
if st.session_state.teclas_der:
    # Detectar el acorde activo
    acorde_actual = None
    for ac in lista_ac:
        if ACORDES_DATA.get(ac, []) == st.session_state.teclas_der:
            acorde_actual = ac
            break
    if acorde_actual:
        st.markdown(explicacion_manos(acorde_actual), unsafe_allow_html=True)
else:
    st.info("Haz clic en un acorde arriba para ver la posición en el piano virtual.")
st.markdown("</div>", unsafe_allow_html=True)





import streamlit as st
import streamlit.components.v1 as components

# 1. ESTILO Y MARCA (KORYM TECH)
st.set_page_config(page_title="KORYMpiano Tutor", layout="wide")
st.markdown("""
<style>
    .creadora { text-align: center; color: #6a1b9a; font-weight: bold; font-size: 2.2em; }
    .status-box { background: #f3e5f5; border-radius: 15px; padding: 20px; border-top: 5px solid #6a1b9a; }
    .piano-container { display: flex; justify-content: center; background: #222; padding: 20px; border-radius: 10px; }
    .key { border: 1px solid #000; text-align: center; line-height: 200px; font-weight: bold; transition: 0.2s; user-select: none; font-size: 12px; }
    .white { width: 50px; height: 180px; background: white; color: #333; }
    .black { width: 30px; height: 110px; background: black; color: white; margin-left: -17px; margin-right: -17px; z-index: 2; }
    /* Colores de Guía Visual */
    .guia-izq { background-color: #bbdefb !important; box-shadow: 0 0 20px #2196f3; } /* AZUL: Mano Izquierda */
    .guia-der { background-color: #c8e6c9 !important; box-shadow: 0 0 20px #4caf50; } /* VERDE: Mano Derecha */
    .correct { background-color: #ffeb3b !important; box-shadow: 0 0 20px #fbc02d; } /* AMARILLO: Bluetooth */
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='creadora'>🎹 KORYMpiano: Tutor Visual de Manos</div>", unsafe_allow_html=True)

# 2. LÓGICA MUSICAL
ACORDES_DATA = {
    'F#': ['F#', 'A#', 'C#'], 'B': ['B', 'D#', 'F#'], 'C#': ['C#', 'F', 'G#'],
    'A#m': ['A#', 'C#', 'F'], 'D#m': ['D#', 'F#', 'A#'], 'G#m': ['G#', 'B', 'D#'],
    'F': ['F', 'A', 'C'], 'Bb': ['A#', 'D', 'F'], 'C': ['C', 'E', 'G'],
    'Am': ['A', 'C', 'E'], 'Dm': ['D', 'F', 'A'], 'Gm': ['G', 'A#', 'D']
}

# 3. BARRA LATERAL
st.sidebar.header("🎓 CONFIGURACIÓN")
video_url = st.sidebar.text_input("YouTube URL:", "https://youtu.be/Xyuuv5co7ko")
acordes_raw = st.sidebar.text_area("Acordes de la canción:", "F# B C# A#m D#m G#m")

# 4. VIDEO
st.video(video_url)

# 5. TECLADO VIRTUAL
if 'teclas_izq' not in st.session_state: st.session_state.teclas_izq = []
if 'teclas_der' not in st.session_state: st.session_state.teclas_der = []

def mostrar_piano(izq, der):
    def clase_guia(n):
        if n in izq: return "guia-izq"
        if n in der: return "guia-der"
        return ""
    
    html_piano = f"""
    <div class="piano-container">
        <div class="key white {clase_guia('C')}" id="C">C</div> <div class="key black {clase_guia('C#')}" id="C#">C#</div>
        <div class="key white {clase_guia('D')}" id="D">D</div> <div class="key black {clase_guia('D#')}" id="D#">D#</div>
        <div class="key white {clase_guia('E')}" id="E">E</div>
        <div class="key white {clase_guia('F')}" id="F">F</div> <div class="key black {clase_guia('F#')}" id="F#">F#</div>
        <div class="key white {clase_guia('G')}" id="G">G</div> <div class="key black {clase_guia('G#')}" id="G#">G#</div>
        <div class="key white {clase_guia('A')}" id="A">A</div> <div class="key black {clase_guia('A#')}" id="A#">A#</div>
        <div class="key white {clase_guia('B')}" id="B">B</div>
    </div>
    <script>
    navigator.requestMIDIAccess({{ bluetooth: true }}).then(access => {{
        for (let input of access.inputs.values()) {{
            input.onmidimessage = (msg) => {{
                const [s, n, v] = msg.data;
                const notas = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
                const tecla = document.getElementById(notas[n % 12]);
                if (s === 144 && v > 0) tecla.classList.add('correct');
                else tecla.classList.remove('correct');
            }};
        }}
    }});
    </script>
    """
    components.html(html_piano, height=230)

# 6. LÓGICA DE BOTONES (RITMO Y TIEMPO)
st.markdown("### 🎶 Toca el acorde según el ritmo del video:")
lista_ac = acordes_raw.split()
cols = st.columns(len(lista_ac))

for i, ac in enumerate(lista_ac):
    if cols[i].button(ac, key=f"btn_{i}"):
        # La izquierda toca la raíz, la derecha la triada
        st.session_state.teclas_der = ACORDES_DATA.get(ac, [])
        st.session_state.teclas_izq = [st.session_state.teclas_der[0]] if st.session_state.teclas_der else []

mostrar_piano(st.session_state.teclas_izq, st.session_state.teclas_der)

# 7. EXPLICACIÓN DEL TUTOR
st.markdown("<div class='status-box'>", unsafe_allow_html=True)
if st.session_state.teclas_der:
    st.write(f"👩‍🏫 **GUÍA DE EJECUCIÓN:**")
    st.write(f"🔵 **Mano Izquierda (Bajo):** Toca la tecla **{st.session_state.teclas_izq[0]}**.")
    st.write(f"🟢 **Mano Derecha (Acorde):** Toca juntas **{' - '.join(st.session_state.teclas_der)}**.")
    st.write("⏱️ **Ritmo:** Sigue el compás del video y cambia de botón cuando escuches el cambio de armonía.")
else:
    st.info("Haz clic en un acorde para ver cómo posicionar tus manos.")
st.markdown("</div>", unsafe_allow_html=True)
