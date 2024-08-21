import subprocess
import cv2
from ultralytics import YOLO


model = YOLO("yolov9c.pt")


# Remplace VIDEO_ID par l'ID de la vidéo YouTube en direct
video_url = "https://www.youtube.com/watch?v=ZIOcuNXfN5o"
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
        results = model(frame)
        
        for result in results:
            boxes = result.boxes  # Boîtes de délimitation
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]  # Coordonnées des coins
                conf = box.conf[0]  # Confiance
                cls = box.cls[0]  # Classe de l'objet détecté

                # Afficher les rectangles de détection et les étiquettes
                label = f"{model.names[int(cls)]}: {conf:.2f}"
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Quitter avec la touche 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'exécution de la commande : {e}")
    print(f"Code de retour : {e.returncode}")
    print(f"Message d'erreur : {e.stderr}")
