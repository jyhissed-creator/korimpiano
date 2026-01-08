import streamlit as st
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN Y ESTILO PROFESIONAL
st.set_page_config(page_title="KORYMpiano Universal", layout="wide")
st.markdown("""
<style>
    .creadora { text-align: center; color: #6a1b9a; font-weight: bold; font-size: 2em; margin-bottom: 20px; }
    .status-box { background: #f3e5f5; border-radius: 15px; padding: 20px; border: 2px solid #6a1b9a; }
    .piano-wrapper { overflow-x: auto; padding: 20px; background: #1a1a1a; border-radius: 15px; }
    .piano-container { display: flex; position: relative; width: 600px; height: 180px; margin: 0 auto; }
    .key { border: 1px solid #000; text-align: center; font-weight: bold; position: relative; cursor: pointer; transition: 0.1s; }
    .white { width: 50px; height: 170px; background: white; color: #333; z-index: 1; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 10px; border-radius: 0 0 5px 5px; }
    .black { width: 30px; height: 100px; background: black; color: white; margin-left: -15px; margin-right: -15px; z-index: 2; border-radius: 0 0 3px 3px; font-size: 0.8em; }
    .active-guide { background-color: #c8e6c9 !important; border-bottom: 10px solid #4caf50; }
    .midi-pressed { background-color: #ffeb3b !important; transform: translateY(2px); }
    .perfect { background-color: #ff5722 !important; color: white; }
</style>
""", unsafe_allow_html=True)

# 2. MOTOR MUSICAL (Sostiene todas las tonalidades)
NOTAS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
# Diccionario base para construir cualquier acorde
MODELO_ACORDES = {
    'MAYOR': [0, 4, 7], 'MENOR': [0, 3, 7], '7MA': [0, 4, 7, 10]
}

def transportar_y_generar(acorde_texto, semitonos):
    es_menor = "m" in acorde_texto
    base = acorde_texto.replace("m", "")
    if base not in NOTAS: return None
    
    # Nueva nota base
    nueva_pos = (NOTAS.index(base) + semitonos) % 12
    nueva_base = NOTAS[nueva_pos]
    
    # Generar notas del acorde
    intervalos = MODELO_ACORDES['MENOR' if es_menor else 'MAYOR']
    notas_acorde = [NOTAS[(nueva_pos + i) % 12] for i in intervalos]
    
    return {"nombre": nueva_base + ("m" if es_menor else ""), "notas": notas_acorde}

# 3. INTERFAZ DE USUARIO
st.markdown("<div class='creadora'>🎹 KORYMpiano Universal Tutor</div>", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configuración")
    url = st.text_input("URL de YouTube:", "https://youtu.be/Xyuuv5co7ko")
    acordes_raw = st.text_area("Lista de acordes (espaciados):", "F# B C# A#m D#m G#m")
    tono_actual = st.selectbox("Tono original de la canción:", NOTAS, index=6) # F# por defecto
    tono_deseado = st.selectbox("Tono para tocar (Transportar a):", NOTAS, index=0) # C por defecto

# Diferencia de semitonos
semitonos = NOTAS.index(tono_deseado) - NOTAS.index(tono_actual)

st.video(url)

# 4. BOTONES DINÁMICOS
if 'acorde_activo' not in st.session_state:
    st.session_state.acorde_activo = {"nombre": "", "notas": []}

st.subheader(f"🎶 Acordes en {tono_deseado}:")
lista_nombres = acordes_raw.split()
cols = st.columns(len(lista_nombres) if lista_nombres else 1)

for i, ac in enumerate(lista_nombres):
    info = transportar_y_generar(ac, semitonos)
    if info and cols[i].button(info['nombre'], key=f"btn_{i}"):
        st.session_state.acorde_activo = info

# 5. PIANO VIRTUAL CON SONIDO Y MIDI
notas_js = ",".join(st.session_state.acorde_activo['notas'])
teclas_html = "".join([f'<div class="key {"black" if "#" in n else "white"} {"active-guide" if n in st.session_state.acorde_activo["notas"] else ""}" id="key-{n}">{n}</div>' for n in NOTAS])

html_final = f"""
<script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>
<div id="status" style="text-align:center; color:white; background:#6a1b9a; padding:10px; border-radius:5px; margin-bottom:10px; cursor:pointer; font-weight:bold;">
    🔊 CLIC PARA ACTIVAR AUDIO Y MIDI
</div>
<div class="piano-wrapper">
    <div class="piano-container">{teclas_html}</div>
</div>
<script>
const synth = new Tone.PolySynth(Tone.Synth).toDestination();
const objetivos = "{notas_js}".split(",");
const status = document.getElementById('status');

status.addEventListener('click', async () => {{
    await Tone.start();
    status.innerText = "🎹 AUDIO LISTO - ESPERANDO PIANO BLUETOOTH";
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
components.html(html_final, height=300)

# 6. EXPLICACIÓN POR MANOS
if st.session_state.acorde_activo['nombre']:
    notas = st.session_state.acorde_activo['notas']
    st.markdown(f"""
    <div class='status-box'>
        <h3>👩‍🏫 Cómo tocar {st.session_state.acorde_activo['nombre']}:</h3>
        <p><b>Mano Izquierda (Bajo):</b> Mantén presionada la nota <b>{notas[0]}</b>.</p>
        <p><b>Mano Derecha (Acorde):</b> Toca al mismo tiempo <b>{', '.join(notas)}</b>.</p>
        <p><i>Sigue el ritmo del video y presiona los botones para cambiar la guía del piano.</i></p>
    </div>
    """, unsafe_allow_html=True)
