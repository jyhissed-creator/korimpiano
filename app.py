import streamlit as st
import streamlit.components.v1 as components

# ================================
# 1. ESTILO Y MARCA (KORYM TECH)
# ================================
st.set_page_config(page_title="KORYMpiano Tutor", layout="wide")

st.markdown("""
<style>
    .creadora { text-align: center; color: #6a1b9a; font-weight: bold; font-size: 2.2em; margin-bottom: 20px; }
    .status-box { background: #f3e5f5; border-radius: 15px; padding: 20px; border-top: 5px solid #6a1b9a; margin-top: 20px; }
    .piano-container { display: flex; justify-content: center; background: #222; padding: 20px; border-radius: 10px; overflow-x: auto; }
    .key { border: 1px solid #000; text-align: center; line-height: 200px; font-weight: bold; transition: 0.2s; user-select: none; font-size: 12px; }
    .white { width: 50px; height: 180px; background: white; color: #333; flex-shrink: 0; }
    .black { width: 30px; height: 110px; background: black; color: white; margin-left: -15px; margin-right: -15px; z-index: 2; flex-shrink: 0; }
    .guia-izq { background-color: #bbdefb !important; box-shadow: 0 0 20px #2196f3; } 
    .guia-der { background-color: #c8e6c9 !important; box-shadow: 0 0 20px #4caf50; } 
    .correct { background-color: #ffeb3b !important; box-shadow: 0 0 20px #fbc02d; } 
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='creadora'>🎹 KORYMpiano: Tutor Visual de Manos</div>", unsafe_allow_html=True)

# ================================
# 2. LÓGICA MUSICAL (DICCIONARIO AMPLIADO)
# ================================
ACORDES_DATA = {
    'C': ['C', 'E', 'G'], 'Cm': ['C', 'D#', 'G'],
    'D': ['D', 'F#', 'A'], 'Dm': ['D', 'F', 'A'],
    'E': ['E', 'G#', 'B'], 'Em': ['E', 'G', 'B'],
    'F': ['F', 'A', 'C'], 'Fm': ['F', 'G#', 'C'],
    'G': ['G', 'B', 'D'], 'Gm': ['G', 'A#', 'D'],
    'A': ['A', 'C#', 'E'], 'Am': ['A', 'C', 'E'],
    'B': ['B', 'D#', 'F#'], 'Bm': ['B', 'D', 'F#'],
    'F#': ['F#', 'A#', 'C#'], 'Bb': ['A#', 'D', 'F'],
    'C#': ['C#', 'F', 'G#'], 'Eb': ['D#', 'G', 'A#'],
    'Ab': ['G#', 'C', 'D#'], 'A#m': ['A#', 'C#', 'F'],
    'D#m': ['D#', 'F#', 'A#'], 'G#m': ['G#', 'B', 'D#']
}

# ================================
# 3. BARRA LATERAL
# ================================
st.sidebar.header("🎓 CONFIGURACIÓN")
video_url = st.sidebar.text_input("YouTube URL:", "https://youtu.be/Xyuuv5co7ko")
# Aquí ya dejamos los acordes listos para que solo los toques
acordes_raw = st.sidebar.text_area("Acordes de la canción:", "F# B C# A#m D#m G#m")

# ================================
# 4. VIDEO
# ================================
st.video(video_url)

# ================================
# 5. TECLADO VIRTUAL E INTEGRACIÓN MIDI
# ================================
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
    if (navigator.requestMIDIAccess) {{
        navigator.requestMIDIAccess({{ bluetooth: true }}).then(access => {{
            for (let input of access.inputs.values()) {{
                input.onmidimessage = (msg) => {{
                    const [s, n, v] = msg.data;
                    const notas = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];
                    const tecla = document.getElementById(notas[n % 12]);
                    if (tecla) {{
                        if (s === 144 && v > 0) tecla.classList.add('correct');
                        else if (s === 128 || (s === 144 && v === 0)) tecla.classList.remove('correct');
                    }}
                }};
            }}
        }});
    }}
    </script>
    """
    components.html(html_piano, height=230)

# ================================
# 6. LÓGICA DE BOTONES (RITMO MEJORADO PARA CELULAR)
# ================================
st.markdown("### 🎶 Toca el acorde según el ritmo del video:")
lista_ac = acordes_raw.split()
if lista_ac:
    # Usamos columnas de 4 en 4 para que se vea bien en celular
    cols = st.columns(4) 
    for i, ac in enumerate(lista_ac):
        with cols[i % 4]:
            if st.button(ac, key=f"btn_{i}", use_container_width=True):
                notas = ACORDES_DATA.get(ac, [])
                if notas:
                    st.session_state.teclas_der = notas
                    st.session_state.teclas_izq = [notas[0]]

mostrar_piano(st.session_state.teclas_izq, st.session_state.teclas_der)

# ================================
# 7. EXPLICACIÓN DEL TUTOR
# ================================
st.markdown("<div class='status-box'>", unsafe_allow_html=True)
if st.session_state.teclas_der:
    st.write("👩‍🏫 **GUÍA DE EJECUCIÓN:**")
    st.write(f"🔵 **Mano Izquierda:** Toca **{st.session_state.teclas_izq[0]}**.")
    st.write(f"🟢 **Mano Derecho:** Toca juntas **{' - '.join(st.session_state.teclas_der)}**.")
else:
    st.info("Haz clic en un acorde para ver cómo posicionar tus manos.")
st.markdown("</div>", unsafe_allow_html=True)
