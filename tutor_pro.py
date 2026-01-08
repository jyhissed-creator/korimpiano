import streamlit as st

# Configuración de la página con tu marca
st.set_page_config(page_title="KORYMpiano by JYHISSED", layout="wide", page_icon="🎹")

# --- ESTILO PERSONALIZADO ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #4CAF50; color: white; }
    .creadora { font-size: 1.2em; color: #6a1b9a; font-weight: bold; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA MUSICAL ---
NOTAS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

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

# --- CRÉDITOS DE LA CREADORA EN LA BARRA LATERAL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3203/3203925.png", width=100)
st.sidebar.title("KORYM Tech")
st.sidebar.markdown("<div class='creadora'>Creado por: JYHISSED (KORYM)</div>", unsafe_allow_html=True)
st.sidebar.write("---")

# --- MENÚ DE NAVEGACIÓN ---
opcion = st.sidebar.radio("Selecciona tu herramienta:", ["🎹 Piano Simple", "🎓 Tutor de Canciones Pro"])

if opcion == "🎹 Piano Simple":
    st.title("🎹 Piano Básico KORYM")
    st.subheader(f"Bienvenida al piano de JYHISSED")
    nota = st.selectbox("Elige una nota para ver su posición:", NOTAS)
    
    st.write(f"### Posición de {nota} en el teclado:")
    # Dibujo de teclado grande
    teclas_grandes = "".join([f"<div style='display:inline-block; border:2px solid black; width:60px; height:200px; background-color:{'#4CAF50' if n == nota else 'white'}; text-align:center; padding-top:160px;'><b>{n}</b></div>" for n in ['C','D','E','F','G','A','B']])
    st.markdown(teclas_grandes, unsafe_allow_html=True)

else:
    st.title("🎼 Tutor de Canciones Profesional")
    st.info("Desarrollado por KORYM Tech para el aprendizaje musical rápido.")
    
    with st.expander("⚙️ CONFIGURACIÓN DE LA CANCIÓN", expanded=True):
        col_video, col_datos = st.columns([2, 1])
        with col_datos:
            video_url = st.text_input("Link de YouTube:", "https://youtu.be/Xyuuv5co7ko")
            tono_orig = st.selectbox("Tono original del texto:", NOTAS, index=5)
            tono_nvo = st.selectbox("¿A qué tono quieres transportarla?", NOTAS, index=6)
        with col_video:
            letra_raw = st.text_area("Pega aquí los acordes (Ej: F Bb C C-Bb-C):", "F Bb C C-Bb-C", height=100)
    
    dif = NOTAS.index(tono_nvo) - NOTAS.index(tono_orig)
    
    if video_url:
        st.video(video_url)
    
    st.header(f"🎶 Guía de Ejecución en {tono_nvo}")
    
    acordes_detectados = [a for a in letra_raw.replace('\n', ' ').split(' ') if a]
    cols = st.columns(len(acordes_detectados))
    
    for i, bloque in enumerate(acordes_detectados):
        with cols[i]:
            st.markdown(f"**Pulso {i+1}**")
            sub_acordes = bloque.split('-')
            for sa in sub_acordes:
                at = transportar(sa, dif)
                st.button(at, key=f"{at}_{i}_{sa}")
                st.caption(f"🫲 Izquierda: {at[0]}")
                
                # Piano Virtual explicativo
                teclas = "".join([f"<div style='display:inline-block; border:1px solid black; width:20px; height:50px; background-color:{'#4CAF50' if n == at[0] else 'white'};'></div>" for n in ['C','D','E','F','G','A','B']])
                st.markdown(teclas, unsafe_allow_html=True)

st.sidebar.write("---")
st.sidebar.caption("© 2024 KORYMpiano - Todos los derechos reservados por JYHISSED.")




