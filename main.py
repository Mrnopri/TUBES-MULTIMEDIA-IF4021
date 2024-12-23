import cv2
import mediapipe as mp
import random
import os
import math
import time

# Menonaktifkan log TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Inisialisasi Mediapipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Fungsi untuk menghitung jarak Euclidean antara dua titik
def euclidean_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

# Fungsi untuk mendeteksi apakah mulut terbuka
def is_mouth_open(landmarks):
    upper_lip = landmarks[13]  # Bibir atas
    lower_lip = landmarks[14]  # Bibir bawah
    distance = euclidean_distance((upper_lip.x, upper_lip.y), (lower_lip.x, lower_lip.y))
    threshold = 0.02
    return distance > threshold

# Fungsi untuk membandingkan pose pengguna dengan pose target dengan presisi
def compare_poses(user_landmarks, target_landmarks):
    if not user_landmarks or not target_landmarks:
        return False

    key_indices = [11, 12, 13, 14, 23, 24]  # Bahu, siku, pinggul
    threshold = 0.05  # Toleransi presisi lebih kecil

    for idx in key_indices:
        user_point = user_landmarks[idx]
        target_point = target_landmarks[idx]
        if abs(user_point.x - target_point.x) > threshold or abs(user_point.y - target_point.y) > threshold:
            return False
    return True

# Fungsi untuk animasi perandoman gambar di area kanan atas
def randomize_images_on_frame(frame, folder_path, duration=5, interval=0.1):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('jpg', 'jpeg', 'png'))]
    if not image_files:
        print("Folder tidak mengandung file gambar.")
        return None

    start_time = time.time()
    selected_image = None
    h, w, _ = frame.shape

    while time.time() - start_time < duration:
        selected_image = random.choice(image_files)
        image_path = os.path.join(folder_path, selected_image)
        image = cv2.imread(image_path)
        resized_image = cv2.resize(image, (200, 200))
        frame[0:200, w-200:w] = resized_image  # Gambar di pojok kanan atas
        cv2.imshow("Random Pose Filter", frame)

        if cv2.waitKey(int(interval * 1000)) & 0xFF == ord('q'):
            break

    return os.path.join(folder_path, selected_image)

# Fungsi utama
def random_pose_filter(target_folder):
    if not os.path.exists(target_folder):
        print(f"Folder {target_folder} tidak ditemukan!")
        return

    cap = cv2.VideoCapture(0)

    success, frame = cap.read()
    if not success:
        print("Gagal membuka kamera!")
        cap.release()
        return

    # Animasi perandoman gambar di pojok kanan atas
    selected_image_path = randomize_images_on_frame(frame, target_folder, duration=2, interval=0.2)
    if not selected_image_path:
        print("Gagal memilih gambar target.")
        cap.release()
        return

    target_image = cv2.imread(selected_image_path)
    if target_image is None:
        print(f"Gagal membaca gambar: {selected_image_path}")
        cap.release()
        return

    # Proses target pose
    target_image_rgb = cv2.cvtColor(target_image, cv2.COLOR_BGR2RGB)
    target_pose_result = pose.process(target_image_rgb)
    target_landmarks = target_pose_result.pose_landmarks.landmark if target_pose_result.pose_landmarks else None
    target_image = cv2.resize(target_image, (200, 200))

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Proses pose dan wajah pengguna
        result = pose.process(frame_rgb)
        user_landmarks = result.pose_landmarks.landmark if result.pose_landmarks else None
        face_results = face_mesh.process(frame_rgb)

        # Tempelkan gambar target di pojok kanan atas
        frame[0:200, -200:] = target_image

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Periksa kecocokan pose
        if compare_poses(user_landmarks, target_landmarks):
            cv2.putText(frame, "Match!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Not Match", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Periksa status mulut dari Face Mesh
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)
                if is_mouth_open(face_landmarks.landmark):
                    cv2.putText(frame, "Mouth Open", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Mouth Closed", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow("Random Pose Filter", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Jalankan program
target_folder = r"D:\\Dingko\\TUBES-MULTIMEDIA-IF4021\\poses"
random_pose_filter(target_folder)
