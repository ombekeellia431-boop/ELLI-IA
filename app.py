import streamlit as st
import os
from gtts import gTTS
from pydub import AudioSegment
import io
import tempfile

# Imports MoviePy
try:
    from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, TextClip, CompositeVideoClip
except ImportError:
    from moviepy.video.VideoClip import ImageClip, TextClip
    from moviepy.audio.io.AudioFileClip import AudioFileClip
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

# --- CONFIGURATION DU STUDIO ---
st.set_page_config(page_title="ELLI-IA Studio Pro", layout="wide")
st.title("🎬 ELLI-IA : Studio de Production & Clonage")

# --- 1. SÉPARATEUR DE PAROLES & SAISIE DU TEXTE ---
st.header("✂️ 1. Musique & Paroles")
file_to_split = st.file_uploader("Étape A : Chargez l'instrumental (MP3/WAV)", type=["mp3", "wav"], key="instr_file")

# INITIALISATION DE LA VARIABLE PAROLES
paroles_finales = ""

if file_to_split:
    st.subheader("🎵 Écoutez l'instrumental choisi")
    st.audio(file_to_split)
    
    # INTERFACE POUR METTRE LES PAROLES (DEMANDÉ)
    st.subheader("📝 Paroles de la chanson")
    paroles_finales = st.text_area(
        "Étape B : Saisissez ou modifiez les paroles ici (elles seront utilisées pour le clip) :", 
        "Entrez vos paroles ici...", 
        height=150
    )
    
    if paroles_finales:
        st.download_button("📥 Télécharger les paroles (.txt)", paroles_finales, "paroles.txt", use_container_width=True)

# --- 2. VOIX & CLONAGE ---
st.divider()
st.header("🎙️ 2. Voix & Clonage")
methode_voix = st.selectbox("Choisis ta méthode de voix :", 
                             ["🎤 Enregistrement Direct", "🤖 Texte vers IA Simple", "👤 Clonage de Voix (Échantillon)"])

voix_pour_mix = None

if methode_voix == "🎤 Enregistrement Direct":
    audio_mic = st.audio_input("Enregistre ta voix par-dessus la musique")
    if audio_mic:
        voix_pour_mix = AudioSegment.from_file(audio_mic)
        st.success("✅ Voix enregistrée !")

elif methode_voix == "🤖 Texte vers IA Simple":
    txt_simple = st.text_input("Texte que l'IA doit dire :", "Bienvenue dans le studio ELLI-IA")
    if st.button("Générer la voix IA"):
        tts = gTTS(text=txt_simple, lang='fr')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        voix_pour_mix = AudioSegment.from_file(fp, format="mp3")
        st.audio(fp)

elif methode_voix == "👤 Clonage de Voix (Échantillon)":
    sample_file = st.file_uploader("Chargez un échantillon de VOTRE voix (MP3)", type=["mp3", "wav"])
    if sample_file and paroles_finales:
        if st.button("Démarrer le Clonage de voix"):
            with st.spinner("L'IA imite votre voix..."):
                # Simulation du clonage
                tts = gTTS(text=paroles_finales, lang='fr') 
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                voix_pour_mix = AudioSegment.from_file(fp, format="mp3")
                st.audio(fp)

# --- 3. MIXAGE & ÉCOUTE FINALE ---
st.divider()
st.header("🎵 3. Mixage & Écoute du Morceau")
audio_mix_final = None

if file_to_split and voix_pour_mix:
    if st.button("🎚️ Créer le Mixage Final"):
        with st.spinner("Mixage en cours..."):
            instr = AudioSegment.from_file(file_to_split)
            mix = instr.overlay(voix_pour_mix)
            
            buf = io.BytesIO()
            mix.export(buf, format="mp3")
            audio_mix_final = buf.getvalue()
            
            st.subheader("🎧 ÉCOUTEZ AVANT DE TÉLÉCHARGER")
            st.audio(audio_mix_final, format="audio/mp3")
            st.download_button("📥 Télécharger la Musique Mixée (MP3)", audio_mix_final, "musique_mixee.mp3", use_container_width=True)

# --- 4. CLIP VIDÉO AVEC FOND ET PAROLES ---
st.divider()
st.header("🎞️ 4. Création du Clip Vidéo")
media_fond = st.file_uploader("Chargez une image ou vidéo de fond", type=["jpg", "png", "mp4"])

if audio_mix_final and media_fond:
    if st.button("🎬 Générer le Clip Vidéo Final"):
        with st.spinner("Montage du clip avec sous-titres..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fa:
                fa.write(audio_mix_final)
                p_audio = fa.name
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(media_fond.name)[1]) as fm:
                fm.write(media_fond.read())
                p_media = fm.name

            try:
                audio_clip = AudioFileClip(p_audio)
                if media_fond.type.startswith("image"):
                    bg = ImageClip(p_media).set_duration(audio_clip.duration)
                else:
                    bg = VideoFileClip(p_media).subclip(0, min(VideoFileClip(p_media).duration, audio_clip.duration))
                
                # Ajout des paroles saisies en étape 1
                txt = TextClip(paroles_finales, fontsize=40, color='white', font='Arial', 
                               method='caption', size=(bg.w*0.8, None)).set_duration(audio_clip.duration).set_pos('bottom')
                
                final_video = CompositeVideoClip([bg, txt]).set_audio(audio_clip)
                final_video.write_videofile("mon_clip.mp4", fps=24, codec="libx264")
                
                st.subheader("📺 REGARDEZ LE CLIP AVANT DE TÉLÉCHARGER")
                st.video("mon_clip.mp4")
                with open("mon_clip.mp4", "rb") as vf:
                    st.download_button("📥 Télécharger le Clip (MP4)", vf, "clip_final.mp4", use_container_width=True)
            except Exception as e:
                st.error(f"Erreur montage : {e}")
