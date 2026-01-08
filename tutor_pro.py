import streamlit as st
import streamlit.components.v1 as components

# ---------------- CONFIGURACIÓN ----------------
st.set_page_config(
    page_title="KORYMpiano by JYHISSED",
    layout="wide",
    page_icon="🎹"
)

# ---------------- ESTILOS ----------------
st.markdown("""
<style>
.main { background-color: #f5f7f9; }

.creadora-header {
    font-size: 2.5em;
    color: #6a1b9a;
    font-weight: bold;
    text-align: center;
}
.sub-header {
    font-size: 1.2em;
    color: #4a148c;
    text-align: center;
    margin-bottom: 20px;
}

.piano {
    display: flex;
    position: relative;
    height: 220px;
    margin: 30px auto;
}

.white {
    width: 60px;
    height: 220px;
    background: white;
    border: 1px solid #000;
    z-index: 1;
    text-align: center;
    line-height: 200px;
    font-weight: bold;
}

.black {
    width: 40px;
    height: 140px;
    background: black;
    position: absolute;
    margin-left: -20px;
    z-index: 2;
}

.key.midi-active {
    background: #2196F3 !important;
    color: white;
}
.black.midi-active {
    background: #1976D2 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='creadora-header'>🎹 KORYMpiano</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Desarrollado por JYHISSED · KORYM Tech</div>", unsafe_allow_html=True)

# ---------------- TECLADO VIRTUAL ----------------
def teclado_virtual():
    html = """
    <div class="piano">
        <div class="key white" id="C" onclick="play(261.63)">C</div>
        <div class="key black" id="C#" style="left:45px" onclick="play(277.18)"></div>

        <div class="key white" id="D" onclick="play(293.66)">D</div>
        <div class="key black" id="D#" style="left:105px" onclick="play(311.13)"></div>

        <div class="key white" id="E" onclick="play(329.63)">E</div>

        <div class="key white" id="F" onclick="play(349.23)">F</div>
        <div class="key black" id="F#" style="left:225px" onclick="play(369.99)"></div>

        <div class="key white" id="G" onclick="play(392.00)">G</div>
        <div class="key black" id="G#" style="left:285px" onclick="play(415.30)"></div>

        <div class="key white" id="A" onclick="play(440.00)">A</div>
        <div class="key black" id="A#" style="left:345px" onclick="play(466.16)"></div>

        <div class="key white" id="B" onclick="play(493.88)">B</div>
    </div>

    <script>
    function play(freq){
        let ctx = new (window.AudioContext || window.webkitAudioContext)();
        let osc = ctx.createOscillator();
        let gain = ctx.createGain();
        osc.frequency.value = freq;
        osc.type = "sine";
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 1);
        osc.stop(ctx.currentTime + 1);
    }
    </script>
    """
    components.html(html, height=260)

st.subheader("🎹 Teclado Virtual Interactivo")
teclado_virtual()

# ---------------- MODO DE APRENDIZAJE ----------------
modo_aprendizaje = st.selectbox(
    "🧠 ¿Cómo quieres aprender?",
    [
        "Muy fácil (principiante)",
        "Con arpegios",
        "Mano derecha",
        "Mano izquierda",
        "Teoría musical",
        "Modo adoración / acompañamiento"
    ]
)

# ---------------- MIDI BLUETOOTH ----------------
def conectar_midi():
    html = """
    <button onclick="connectMIDI()">🎹 Conectar Piano Bluetooth</button>
    <p id="status"></p>

    <script>
    const notas = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'];

    function midiToNote(midi){
        return notas[midi % 12];
    }

    function connectMIDI(){
        navigator.requestMIDIAccess().then(access => {
            document.getElementById("status").innerText = "🎹 Piano conectado";

            for (let input of access.inputs.values()){
                input.onmidimessage = function(msg){
                    let note = msg.data[1];
                    let velocity = msg.data[2];
                    let noteName = midiToNote(note);
                    let key = document.getElementById(noteName);

                    if (!key) return;

                    if (velocity > 0){
                        key.classList.add("midi-active");
                    } else {
                        key.classList.remove("midi-active");
                    }
                }
            }
        }).catch(() => {
            document.getElementById("status").innerText = "❌ No se pudo conectar";
        });
    }
    </script>
    """
    components.html(html, height=120)

st.subheader("🔗 Conecta tu piano Bluetooth")
conectar_midi()

# ---------------- AUTORÍA ----------------
st.markdown("""
### 👩‍🎹 Creadora  
**JYHISSED**  
*KORYM Tech*  
Desarrolladora de **KORYMpiano**
""")

st.sidebar.caption("© KORYMpiano by JYHISSED · KORYM Tech")
