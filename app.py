
import streamlit as st
from music21 import note, stream, tempo, midi
import random
import os
from gtts import gTTS
import numpy as np
from pydub import AudioSegment
import io

# --- CONFIGURATION ---
st.set_page_config(page_title="ELLI-IA Studio Pro", layout="wide")
st.header("🎬 ELLI-IA : Studio de Séparation & Création")

# --- FONCTION DE SÉPARATION (LÉGÈRE) ---
def separer_voix(audio_file):
    # Charger l'audio
    sound = AudioSegment.from_file(audio_file)
    # Séparer en deux canaux (stéréo)
    channels = sound.split_to_mono()
    if len(channels) < 2:
        return sound # Pas possible de séparer si c'est déjà du mono
    
    # Inversion de phase pour isoler le centre (souvent la voix)
    # Note : C'est une méthode simplifiée pour ne pas faire planter le serveur
    voix_isolee = channels[0].overlay(channels[1].invert_phase())
    return voix_isolee

# --- SECTION 1 : SÉPARATEUR DE PAROLES ---
st.subheader("✂️ 1. Séparateur de Paroles & Instrumental")
uploaded_audio = st.file_uploader("Chargez une chanson (MP3 ou WAV)", type=["mp3", "wav"])

if uploaded_audio:
    st.audio(uploaded_audio)
    if st.button("🚀 Extraire les paroles maintenant"):
        with st.spinner("Extraction en cours..."):
            try:
                resultat = separer_voix(uploaded_audio)
                
                # Sauvegarde en mémoire
                buffer = io.BytesIO()
                resultat.export(buffer, format="mp3")
                
                st.success("Extraction terminée !")
                st.audio(buffer)
                
                # Bouton de téléchargement
                st.download_button(
                    label="📥 Télécharger les paroles extraites",
                    data=buffer.getvalue(),
                    file_name="paroles_extraites_elli_ia.mp3",
                    mime="audio/mp3"
                )
            except Exception as e:
                st.error(f"Erreur technique : {e}. Assurez-vous d'utiliser un fichier stéréo.")

# --- SECTION 2 : CRÉATION AVEC LES NOUVELLES PAROLES ---
st.divider()
st.subheader("📝 2. Créer une chanson avec ces paroles")
text_area = st.text_area("Écrivez ou modifiez les paroles extraites :", "Tapez ici...")

col1, col2 = st.columns(2)
with col1:
    if st.button("🎙️ Générer la Voix IA"):
        tts = gTTS(text=text_area, lang='fr')
        tts.save("ma_voix.mp3")
        st.audio("ma_voix.mp3")

with col2:
    if st.button("🎹 Générer l'Instrumental"):
        s = stream.Stream()
        for i in range(12):
            n = note.Note(random.choice(['C4', 'E4', 'G4', 'A4']))
            s.append(n)
        mf = midi.translate.streamToMidiFile(s)
        mf.open("instru.mid", 'wb')
        mf.write()
        mf.close()
        st.success("Mélodie prête !")

# --- VIDÉO DE PRÉSENTATION ---
try:
    with open('video.mp4', 'rb') as v:
        st.video(v.read())
except:
    st.info("Vidéo de présentation ELLI-IA prête pour le chargement.")
