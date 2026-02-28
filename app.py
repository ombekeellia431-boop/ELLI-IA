<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Lecteur avec Durée</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #eceff1; padding: 30px; text-align: center; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 15px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }
        .media-block { margin-bottom: 30px; padding: 15px; border-bottom: 1px solid #eee; }
        .duration-badge { background: #34495e; color: white; padding: 4px 10px; border-radius: 20px; font-size: 0.9em; margin-bottom: 10px; display: inline-block; }
        video, audio { width: 100%; border-radius: 8px; margin-top: 10px; }
        .download-link { display: block; margin-top: 15px; color: #2980b9; font-weight: bold; text-decoration: none; }
    </style>
</head>
<body>

<div class="container">
    <h2>🎵 Studio de Prévisualisation</h2>

    <div class="media-block">
        <span id="audio-duration" class="duration-badge">Durée : calcul...</span>
        <audio id="myAudio" controls>
            <source src="votre-audio.mp3" type="audio/mpeg">
        </audio>
        <a href="votre-audio.mp3" download class="download-link">📥 Télécharger l'Audio</a>
    </div>

    <div class="media-block">
        <span id="video-duration" class="duration-badge">Durée : calcul...</span>
        <video id="myVideo" controls>
            <source src="votre-video.mp4" type="video/mp4">
        </video>
        <a href="votre-video.mp4" download class="download-link">📥 Télécharger la Vidéo</a>
    </div>
</div>

<script>
    // Fonction pour formater les secondes en MM:SS
    function formatTime(seconds) {
        let min = Math.floor(seconds / 60);
        let sec = Math.floor(seconds % 60);
        if (sec < 10) sec = "0" + sec;
        return min + ":" + sec;
    }

    // Récupérer la durée de l'audio
    const audio = document.getElementById('myAudio');
    audio.addEventListener('loadedmetadata', function() {
        document.getElementById('audio-duration').innerText = "Durée : " + formatTime(audio.duration);
    });

    // Récupérer la durée de la vidéo
    const video = document.getElementById('myVideo');
    video.addEventListener('loadedmetadata', function() {
        document.getElementById('video-duration').innerText = "Durée : " + formatTime(video.duration);
    });
</script>

</body>
</html>

