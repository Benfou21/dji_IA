import subprocess
import cv2

# Remplace VIDEO_ID par l'ID de la vidéo YouTube en direct
video_url = "https://www.youtube.com/live/DeXhxJOt4gY"
command = ["yt-dlp", "-g", video_url]

# Exécuter la commande et capturer l'URL du flux
try:
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    url_m3u8 = result.stdout.strip()

    print("URL du flux m3u8:", url_m3u8)

    # Lire le flux vidéo avec OpenCV
    cap = cv2.VideoCapture(url_m3u8)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur : Impossible de lire le flux vidéo")
            break

        # Afficher la frame
        cv2.imshow('Live Stream', frame)

        # Quitter avec la touche 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'exécution de la commande : {e}")
    print(f"Code de retour : {e.returncode}")
    print(f"Message d'erreur : {e.stderr}")
