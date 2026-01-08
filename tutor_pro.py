import streamlit as st

# Configuración de la página con tu marca
st.set_page_config(page_title="KORYMpiano by JYHISSED", layout="wide", page_icon="🎹")

# --- ESTILO PERSONALIZADO ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4CAF50; color: white; }
    .creadora { font-size: 1.2em; color: #6a1b9a; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .arpegio-box { background-color: #e1f5fe; border-left: 5px solid #03a9f4; padding: 10px; border-radius: 5px; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA MUSICAL ---
NOTAS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

def obtener_notas_acorde(base):
    # Lógica simple para obtener 1ra, 3ra y 5ta (Arpegio básico mayor)
    idx = NOTAS.index(base)
    tercera = NOTAS[(idx + 4) % 12]
    quinta = NOTAS[(idx + 7) % 12]
    octava = base
    return [base, tercera, quinta, octava]

def transportar(acorde, semitonos):
    try:
        a = acorde.strip().capitalize()
        base = a[0]
        if len(a) > 1 and a[1] in ['#', 'b', 'B']:
            base = a[:2].replace('b', '#').replace('B', '#')
        idx = NOTAS.index(base)
        nueva = NOTAS[(idx + semitonos) % 12]
        return nueva + a[len(base):]
    except: return acorde

# --- CRÉDITOS EN LA BARRA LATERAL ---
st.sidebar.title("KORYM Tech")
st.sidebar.markdown("<div class='creadora'>Creado por: JYHISSED (KORYM)</div>", unsafe_allow_html=True)

# --- OPCIÓN DE ARPEGIO Y BLUETOOTH ---
st.sidebar.write("---")
st.sidebar.subheader("🎚️ Ajustes Avanzados")
modo_arpegio = st.sidebar.toggle("Activar Modo Arpegio", help="Muestra el orden de las notas para tocar arpegiado")
conectividad = st.sidebar.selectbox("Conectividad:", ["Teclado Local", "Bluetooth MIDI (Beta)"])

opcion = st.sidebar.radio("Herramienta:", ["🎹 Piano Simple", "🎓 Tutor de Canciones Pro"])

if opcion == "🎹 Piano Simple":
    st.title("🎹 Piano Básico KORYM")
    st.subheader(f"Bienvenida al piano de JYHISSED")
    nota = st.selectbox("Elige una nota:", NOTAS)
    
    if modo_arpegio:
        notas_arp = obtener_notas_acorde(nota)
        st.info(f"✨ Arpegio de {nota}: " + " → ".join(notas_arp))
    
    teclas_grandes = "".join([f"<div style='display:inline-block; border:2px solid black; width:60px; height:200px; background-color:{'#4CAF50' if n == nota else 'white'}; text-align:center; padding-top:160px;'><b>{n}</b></div>" for n in ['C','D','E','F','G','A','B']])
    st.markdown(teclas_grandes, unsafe_allow_html=True)

else:
    st.title("🎼 Tutor de Canciones Profesional")
    with st.expander("⚙️ CONFIGURACIÓN", expanded=True):
        video_url = st.text_input("Link de YouTube:", "https://youtu.be/Xyuuv5co7ko")
        col1, col2 = st.columns(2)
        with col1: tono_orig = st.selectbox("Tono original:", NOTAS, index=5)
        with col2: tono_nvo = st.selectbox("Transportar a:", NOTAS, index=6)
        letra_raw = st.text_area("Acordes:", "F Bb C C-Bb-C")

    dif = NOTAS.index(tono_nvo) - NOTAS.index(tono_orig)
    if video_url: st.video(video_url)
    
    st.header(f"🎶 Guía en {tono_nvo}")
    acordes_detectados = [a for a in letra_raw.replace('\n', ' ').split(' ') if a]
    cols = st.columns(len(acordes_detectados))
    
    for i, bloque in enumerate(acordes_detectados):
        with cols[i]:
            for sa in bloque.split('-'):
                at = transportar(sa, dif)
                st.button(at, key=f"{at}_{i}_{sa}")
                
                # Visualización de Arpegio
                if modo_arpegio:
                    base_nota = at[0] if len(at)==1 or at[1] not in ['#','b'] else at[:2]
                    notas_a = obtener_notas_acorde(base_nota)
                    st.markdown(f"""<div class='arpegio-box'><b>Arpegio:</b><br>{' - '.join(notas_a)}</div>""", unsafe_allow_html=True)
                
                st.caption(f"🫲 Izq (Bajo): {at[0]}")
                teclas = "".join([f"<div style='display:inline-block; border:1px solid black; width:20px; height:50px; background-color:{'#4CAF50' if n == at[0] else 'white'};'></div>" for n in ['C','D','E','F','G','A','B']])
                st.markdown(teclas, unsafe_allow_html=True)

st.sidebar.write("---")
st.sidebar.caption("© 2024 KORYMpiano - JYHISSED.")
