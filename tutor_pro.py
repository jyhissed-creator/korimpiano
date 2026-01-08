import streamlit as st
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN Y MARCA
st.set_page_config(page_title="KORYMpiano by JYHISSED", layout="wide", page_icon="🎹")

st.markdown("""
<style>
    .creadora-header { font-size: 2.5em; color: #6a1b9a; font-weight: bold; text-align: center; }
    .sub-header { font-size: 1.2em; color: #4a148c; text-align: center; margin-bottom: 20px; }
    .piano { display: flex; position: relative; height: 200px; margin: 20px auto; justify-content: center; }
    .white { width: 50px; height: 200px; background: white; border: 1px solid #000; z-index: 1; text-align: center; line-height: 180px; font-weight: bold; }
    .black { width: 35px; height: 120px; background: black; position: absolute; margin-left: -17px; z-index: 2; }
    .instruccion-caja { background-color: #f0f2f6; border-left: 5px solid #6a1b9a; padding: 15px; border-radius: 10px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='creadora-header'>🎹 KORYMpiano</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Desarrollado por JYHISSED · KORYM Tech</div>", unsafe_allow_html=True)

# 2. LOGICA MUSICAL Y DICCIONARIO DE POSICIONES
NOTAS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# Diccionario para explicar cómo poner las manos
POSICIONES = {
    'C': "Do - Mi - Sol", 'C#': "Do# - Fa - Sol#", 'D': "Re - Fa# - La",
    'D#': "Re# - Sol - La#", 'E': "Mi - Sol# - Si", 'F': "Fa - La - Do",
    'F#': "Fa# - La# - Do#", 'G': "Sol - Si - Re", 'G#': "Sol# - Do - Re#",
    'A': "La - Do# - Mi", 'A#': "La# - Re - Fa", 'B': "Si - Re# - Fa#"
}

def transportar(acorde, semitonos):
    try:
        a = acorde.strip().capitalize()
        base = a[:2] if len(a) > 1 and a[1] in ['#', 'b'] else a[0]
        base = base.replace('b', '#')
        idx = NOTAS.index(base)
        nueva = NOTAS[(idx + semitonos) % 12]
        return nueva + a[len(base):]
    except: return acorde

# 3. BARRA LATERAL (TUTOR DE YOUTUBE)
st.sidebar.header("🎓 TUTOR PRO")
video_url = st.sidebar.text_input("Link de YouTube:", "https://youtu.be/Xyuuv5co7ko")
tono_orig = st.sidebar.selectbox("Tono original:", NOTAS, index=0)
tono_nvo = st.sidebar.selectbox("Transportar a:", NOTAS, index=0)
letra_raw = st.sidebar.text_area("Escribe los acordes (separados por espacio):", "C G Am F")

# 4. TECLADO VIRTUAL
def teclado_virtual():
    html = """
    <div class="piano">
        <div class="key white" id="C">C</div> <div class="key black" id="C#" style="left:35px"></div>
        <div class="key white" id="D" style="margin-left:5px">D</div> <div class="key black" id="D#" style="left:90px"></div>
        <div class="key white" id="E" style="margin-left:5px">E</div>
        <div class="key white" id="F" style="margin-left:5px">F</div> <div class="key black" id="F#" style="left:195px"></div>
        <div class="key white" id="G" style="margin-left:5px">G</div> <div class="key black" id="G#" style="left:250px"></div>
        <div class="key white" id="A" style="margin-left:5px">A</div> <div class="key black" id="A#" style="left:305px"></div>
        <div class="key white" id="B" style="margin-left:5px">B</div>
    </div>
    """
    components.html(html, height=230)

teclado_virtual()

# 5. CONECTOR BLUETOOTH
if st.button("🔗 CONECTAR PIANO BLUETOOTH"):
    st.balloons()
    js_midi = """
    <script>
    navigator.requestMIDIAccess({ bluetooth: true }).then(access => {
        for (let input of access.inputs.values()){
            input.onmidimessage = (msg) => {
                let [type, note, velocity] = msg.data;
                let noteName = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][note % 12];
                let key = window.parent.document.getElementById(noteName);
                if (key) {
                    if (type === 144 && velocity > 0) key.style.backgroundColor = "#4CAF50";
                    else key.style.backgroundColor = key.id.includes('#') ? "black" : "white";
                }
            }
        }
    });
    </script>
    """
    components.html(js_midi, height=0)

# 6. MOSTRAR CANCIÓN Y ACORDES TRANSPORTADOS
if video_url:
    st.video(video_url)

dif = NOTAS.index(tono_nvo) - NOTAS.index(tono_orig)
st.subheader(f"🎶 Guía para tocar en tono {tono_nvo}:")

acordes_lista = letra_raw.split()
cols = st.columns(len(acordes_lista) if len(acordes_lista) > 0 else 1)

# Variable para guardar cuál acorde se hizo clic para mostrar la ayuda
acorde_seleccionado = None

for i, acc in enumerate(acordes_lista):
    nuevo_acc = transportar(acc, dif)
    if cols[i % len(cols)].button(nuevo_acc, key=f"btn_{i}"):
        acorde_seleccionado = nuevo_acc

# 7. EXPLICACIÓN DE MANOS (EL TUTOR)
if acorde_seleccionado:
    base = acorde_seleccionado[:2] if len(acorde_seleccionado) > 1 and acorde_seleccionado[1] == '#' else acorde_seleccionado[0]
    notas_guia = POSICIONES.get(base, "Posición no definida")
    
    st.markdown(f"""
    <div class="instruccion-caja">
        <h4>👩‍🏫 Cómo tocar el acorde <b>{acorde_seleccionado}</b>:</h4>
        <p><b>Mano Izquierda (Bajo):</b> Toca la tecla <b>{base}</b> en la parte más grave del piano.</p>
        <p><b>Mano Derecha (Acorde):</b> Toca estas tres notas juntas: <b>{notas_guia}</b>.</p>
        <p><i>Tip: Mantén el pedal presionado para que suene más profesional.</i></p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("Haz clic en cualquier acorde de arriba para ver cómo poner las manos.")

st.markdown(f"--- \n**Creadora:** JYHISSED | KORYM Tech")
