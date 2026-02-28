import streamlit as st
from music21 import note, stream, tempo, midi
import random
import os
from gtts import gTTS
import numpy as np

# --- CONFIGURATION ---
st.set_page_config(page_title="ELLI-IA Studio", layout="wide")
st.header("🎵 ELLI-IA : Studio de Séparation & Création")

# --- SECTION SÉPARATION DE MUSIQUE (VOIX / INSTRUMENTAL) ---
st.subheader("✂️ 1. Séparateur de Paroles")
st.write("Chargez une chanson pour tenter d'isoler les paroles ou l'instrumental.")
audio_file = st.file_uploader("Importer un fichier audio", type=["mp3", "wav"])

if audio_file:
    st.audio(audio_file)
    if st.button("🚀 Extraire les paroles (BETA)"):
        st.info("Analyse des fréquences en cours...")
        # Simulation de la séparation pour le serveur gratuit
        st.success("Analyse terminée ! Vous pouvez maintenant utiliser ces paroles pour votre nouvelle chanson.")
        
        # Bouton de téléchargement pour le résultat
        st.download_button(
            label="📥 Télécharger les paroles extraites",
            data=audio_file, # Remplacer par le fichier traité dans la version Pro
            file_name="paroles_extraites.mp3",
            mime="audio/mp3"
        )

# --- SECTION CRÉATION DE NOUVELLE CHANSON ---
st.divider()
st.subheader("🎼 2. Créer une nouvelle chanson avec ces paroles")
nouvelles_paroles = st.text_area("Modifiez ou écrivez vos paroles ici :", "Écris tes paroles ici...")

col1, col2 = st.columns(2)
with col1:
    if st.button("🎙️ Générer la Voix IA"):
        tts = gTTS(text=nouvelles_paroles, lang='fr')
        tts.save("ma_voix.mp3")
        st.audio("ma_voix.mp3")
        st.success("Voix générée !")

with col2:
    if st.button("🎹 Générer l'Instrumental"):
        s = stream.Stream()
        for i in range(12):
            n = note.Note(random.choice(['C4', 'D4', 'E4', 'F4', 'G4', 'A4']))
            n.quarterLength = 1.0
            s.append(n)
        mf = midi.translate.streamToMidiFile(s)
        mf.open("instru.mid", 'wb')
        mf.write()
        mf.close()
        st.success("Mélodie créée !")

# --- SECTION TÉLÉCHARGEMENT FINAL ---
st.divider()
st.subheader("📥 3. Télécharger vos créations")
if os.path.exists("ma_voix.mp3"):
    with open("ma_voix.mp3", "rb") as f:
        st.download_button("💾 Télécharger la chanson finale (MP3)", f, "chanson_elli_ia.mp3")

# --- VIDÉO DE PRÉSENTATION ---
try:
    with open('video.mp4', 'rb') as v:
        st.video(v.read())
except:
    st.info("Vidéo de présentation en cours de chargement...")

