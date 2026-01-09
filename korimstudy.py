import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Korim.piano.&Studio")

st.markdown("""
    <style>
    .stApp { background: #000; }
    iframe { border: none !important; }
    </style>
""", unsafe_allow_html=True)

# SISTEMA DE GENERACIÓN INTERNA DE AUDIO
korim_v4_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>
    <style>
        :root { --korim: #00ff88; --accent: #6a00ff; }
        body { background: #000; color: #fff; font-family: sans-serif; margin: 0; padding: 10px; text-align: center; touch-action: manipulation; }
        
        .header { margin: 15px 0; }
        .brand { font-size: 22px; font-weight: 900; color: var(--korim); text-transform: uppercase; }
        .creator { font-size: 10px; letter-spacing: 4px; color: var(--accent); font-weight: bold; }
        
        .box { background: #0a0a0a; border: 1px solid #222; border-radius: 15px; padding: 20px; max-width: 600px; margin: 0 auto; }
        
        .btn-main { background: #ff4b00; color: white; width: 100%; padding: 15px; border-radius: 10px; border: none; font-weight: bold; margin-bottom: 15px; box-shadow: 0 0 20px rgba(255,75,0,0.3); }
        
        textarea { width: 100%; height: 90px; background: #000; color: var(--korim); border: 1px solid #333; border-radius: 8px; padding: 10px; font-size: 16px; margin-bottom: 10px; box-sizing: border-box; }
        
        .controls { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        .btn-play { background: var(--korim); color: black; font-weight: bold; padding: 12px; border-radius: 8px; border: none; }
        .btn-stop { background: #333; color: white; padding: 12px; border-radius: 8px; border: none; }

        #piano-container { overflow-x: auto; margin-top: 20px; padding-bottom: 10px; }
        #piano { display: inline-flex; height: 140px; border-radius: 5px; overflow: hidden; }
        .key { border: 1px solid #111; position: relative; flex-shrink: 0; }
        .white { width: 40px; height: 100%; background: #fff; }
        .black { width: 26px; height: 85px; background: #222; margin-left: -13px; margin-right: -13px; z-index: 2; border-radius: 0 0 3px 3px; }
        .hit { background: var(--korim) !important; box-shadow: 0 0 20px var(--korim); transform: translateY(3px); }
        
        #lyric-view { background: #050505; border-radius: 10px; padding: 15px; margin: 15px 0; text-align: left; border-left: 4px solid var(--korim); min-height: 50px; }
        .chord { color: var(--korim); font-weight: bold; }
    </style>
</head>
<body>

    <div class="header">
        <div class="brand">Korim.piano.&Studio</div>
        <div class="creator">BY YHISSED JIMÉNEZ</div>
    </div>

    <div class="box">
        <button class="btn-main" id
        
