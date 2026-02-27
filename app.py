
import streamlit as st
from music21 import note, stream, tempo, midi, text
import random
import os
from gtts import gTTS # Import gTTS
# --- AJOUT DE TA VIDÉO ET TON NOM ---
st.header("Bienvenue dans le studio de ELLI-IA") # Ton nom ici
st.write("Voici ma musique et ma présentation :")

# Affichage de ta vidéo (assure-toi que le fichier s'appelle bien video.mp4 sur GitHub)
try:
    video_file = open('video.mp4', 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)
except:
    st.info("Chargement de la vidéo en cours...")

# --- CLONAGE DE VOIX LÉGER (SIMULATION) ---
st.subheader("🎙️ Personnalisation de la Voix")
option_voix = st.selectbox("Choisis le timbre de voix :", ["Voix Studio", "Voix Robot", "Voix Douce"])

def generate_light_cloning(text, type_voix):
    # On utilise gTTS (déjà présent ligne 6) pour rester léger
    tts = gTTS(text=text, lang='fr', slow=(type_voix == "Voix Douce"))
    tts.save("voice_output.mp3")
    return "voice_output.mp3"

if st.button("Générer la voix"):
    # On récupère le texte des paroles que tu as déjà dans ton code
    audio_path = generate_light_cloning("Bienvenue sur elliamusic", option_voix)
    st.audio(audio_path)

st.divider() # Petite ligne pour séparer de la suite
# ------------------------------------

st.set_page_config(layout="wide")

st.title("AI Music Generation Application")
st.write("This interactive application allows you to generate music using AI models and download the audio files.")

def generate_simple_melody(num_notes=8, min_pitch=60, max_pitch=72, duration=0.5, bpm=120, lyrics=None):
    s = stream.Stream()
    s.append(tempo.MetronomeMark(number=bpm))

    lyric_words = []
    if lyrics:
        lyric_words = [word for word in lyrics.split() if word.strip()]

    for i in range(num_notes):
        pitch = random.randint(min_pitch, max_pitch)
        n = note.Note(pitch)
        n.duration.quarterLength = duration

        if lyric_words and i < len(lyric_words):
            n.addLyric(lyric_words[i])
        elif lyric_words and i >= len(lyric_words):
            n.addLyric(lyric_words[i % len(lyric_words)])

        s.append(n)
    return s

def generate_simple_lyrics(num_lines: int = 4, seed_word: str = "") -> str:
    subjects = ["sun", "moon", "star", "dream", "heart", "melody", "soul", "sky", "river"]
    verbs = ["shines", "sings", "flows", "dreams", "whispers", "dances", "glows", "flies"]
    adjectives = ["bright", "gentle", "soft", "golden", "endless", "sweet", "deep", "silent"]
    objects = ["night", "day", "song", "love", "hope", "light", "peace", "time"]

    lyrics_lines = []
    for i in range(num_lines):
        adjective = random.choice(adjectives)
        subject = random.choice(subjects)
        verb = random.choice(verbs)
        obj = random.choice(objects)

        line = f"The {adjective} {subject} {verb} {obj}."
        lyrics_lines.append(line)

    if seed_word and lyrics_lines:
        target_line_index = random.randint(0, len(lyrics_lines) - 1)
        original_line = lyrics_lines[target_line_index]
        words_in_line = original_line.replace('.', '').split()

        if len(words_in_line) > 1:
            word_to_replace_index = random.randint(1, len(words_in_line) - 1)
            words_in_line[word_to_replace_index] = seed_word
            lyrics_lines[target_line_index] = ' '.join(words_in_line) + '.'
        else:
            lyrics_lines[target_line_index] = f"{original_line[:-1]} {seed_word}."

    return "\n" .join(lyrics_lines)
def generate_speech_from_lyrics(lyrics_text: str, lang: str = 'en') -> str:
    if not lyrics_text.strip():
        return ""
    try:
        tts = gTTS(text=lyrics_text, lang=lang, slow=False)
        output_file = "generated_speech.mp3"
        tts.save(output_file)
        return output_file
    except Exception as e:
        st.error(f"Error generating speech: {e}")
        return ""


# Streamlit UI for melody generation
st.header("Generate Simple Melody")

num_notes = st.slider("Number of Notes", min_value=1, max_value=20, value=8, key="melody_num_notes")
min_pitch = st.slider("Minimum Pitch (MIDI)", min_value=24, max_value=84, value=60, key="melody_min_pitch")
max_pitch = st.slider("Maximum Pitch (MIDI)", min_value=24, max_value=84, value=72, key="melody_max_pitch")
duration = st.slider("Note Duration (quarter lengths)", min_value=0.1, max_value=4.0, value=0.5, step=0.1, key="melody_duration")
bpm = st.slider("Tempo (BPM)", min_value=60, max_value=240, value=120, key="melody_bpm")

# --- New Section for Lyric Generation ---
st.header("Génération de Paroles")

lyric_input_method = st.radio(
    "Choisissez votre méthode de saisie des paroles:",
    ("Saisie Manuelle", "Génération par IA"),
    key="lyric_input_method"
)

if 'current_lyrics' not in st.session_state:
    st.session_state['current_lyrics'] = ""

if lyric_input_method == "Saisie Manuelle":
    custom_lyrics = st.text_area("Entrez vos paroles ici:", height=150, value=st.session_state['current_lyrics'], key="custom_lyrics_input")
    if st.button("Utiliser ces Paroles", key="use_custom_lyrics_button"):
        st.success("Paroles manuelles enregistrées!")
        st.session_state['current_lyrics'] = custom_lyrics
else: # Génération par IA
    st.write("Générer des paroles automatiquement à partir de mots-clés.")
    num_lyric_lines = st.slider("Nombre de lignes de paroles à générer", min_value=1, max_value=10, value=4, key="ai_lyric_lines")
    lyric_seed = st.text_input("Mot ou phrase d'amorçage pour la génération (optionnel)", "", key="ai_lyric_seed")
    if st.button("Générer des Paroles par IA", key="generate_ai_lyrics_button"):
        generated_lyrics = generate_simple_lyrics(num_lines=num_lyric_lines, seed_word=lyric_seed)
        st.text_area("Paroles générées:", value=generated_lyrics, height=150, disabled=True, key="generated_lyrics_display")
        st.success("Paroles IA générées!")
        st.session_state['current_lyrics'] = generated_lyrics

if st.session_state['current_lyrics']:
    st.subheader("Paroles Actuelles:")
    st.write(st.session_state['current_lyrics'])
    
    # Add a button to generate speech from lyrics
    if st.button("Générer la Voix à partir des Paroles", key="generate_speech_button"):
        speech_file_path = generate_speech_from_lyrics(st.session_state['current_lyrics'], lang='fr') # Use French language for gTTS
        if speech_file_path:
            st.success(f"Voix générée et sauvegardée sous {speech_file_path}")
            with open(speech_file_path, "rb") as file:
                st.audio(file.read(), format="audio/mp3", start_time=0)
                st.download_button(
                    label="Télécharger l'Audio des Paroles",
                    data=file,
                    file_name="generated_speech.mp3",
                    mime="audio/mp3"
                )


if st.button("Generate Melody with Lyrics (if provided)", key="final_generate_button"):
    melody = generate_simple_melody(
        num_notes=num_notes,
        min_pitch=min_pitch,
        max_pitch=max_pitch,
        duration=duration,
        bpm=bpm,
        lyrics=st.session_state['current_lyrics'] if st.session_state['current_lyrics'] else None
    )
    midi_file_path = "generated_melody_with_lyrics.mid"
    melody.write('midi', fp=midi_file_path)

    st.success(f"Mélodie avec paroles générée et sauvegardée sous {midi_file_path}")

    with open(midi_file_path, "rb") as file:
        btn = st.download_button(
            label="Download MIDI with Lyrics",
            data=file,
            file_name="generated_melody_with_lyrics.mid",
            mime="audio/midi"
        )
