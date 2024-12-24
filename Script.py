import cv2
import os

def extract_frames(video_path, output_folder, interval=1):
    """
    Extrait des frames d'une vidéo à des intervalles donnés.

    :param video_path: Chemin de la vidéo d'entrée.
    :param output_folder: Dossier de sortie pour les images.
    :param interval: Intervalle en secondes entre chaque frame.
    """
    # Assurez-vous que le dossier de sortie existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Charger la vidéo
    video_capture = cv2.VideoCapture(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)  # Récupérer la fréquence d'images
    frame_interval = int(fps * interval)  # Calculer l'intervalle en nombre de frames

    frame_count = 0
    saved_frame_count = 0

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break  # Arrêter si la vidéo est terminée

        # Sauvegarder la frame si elle correspond à l'intervalle
        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{saved_frame_count:04d}.png")
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1

        frame_count += 1

    # Libérer les ressources
    video_capture.release()
    print(f"Extraction terminée. {saved_frame_count} frames sauvegardées dans {output_folder}.")

# Exemple d'utilisation
video_path = "/Users/noedaniel/Downloads/VideoAlice//Users/noedaniel/Downloads/VideoAlice/VideoAlice copie.mp4"  # Chemin vers votre fichier vidéo
output_folder = "/Users/noedaniel/Downloads/VideoAlice/"  # Dossier où sauvegarder les frames
extract_frames(video_path, output_folder, interval=1)  # Extraire une frame toutes les 1 seconde