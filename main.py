import cv2
import mediapipe as mp
import pickle
import os
import random
import time
import feature_extractor

# Inisialisasi Mediapipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Fungsi untuk menghitung jarak Euclidean
def euclidean_distance(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

# Fungsi untuk membandingkan fitur
def compare_features(user_features, target_features):
    threshold = 0.03
    for user_feature in user_features:
        for key in user_feature:
            if abs(user_feature[key] - target_features[key]) > threshold:
                return False
    return True

# Fungsi untuk merandom gambar
def randomize_image(folder_path):
    image_files = [f for f in os.listdir(folder_path) if f.endswith(('jpg', 'jpeg', 'png'))]
    if not image_files:
        print("Folder tidak mengandung file gambar.")
        return None
    selected_image = random.choice(image_files)
    return os.path.join(folder_path, selected_image)

# Fungsi utama
def main():
    # Load fitur target dari file pickle
    if not os.path.exists("features.pkl"):
        print("File features.pkl tidak ditemukan. Jalankan pickle.py terlebih dahulu untuk menyimpan fitur target.")
        return

    with open("features.pkl", "rb") as f:
        target_features = pickle.load(f)

    # Folder tempat gambar pose
    target_folder = r"D:\\Dingko\\TUBES-MULTIMEDIA-IF4021\\poses"
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Gagal membuka kamera!")
        return

    # Ambil semua file gambar dari folder
    image_files = [os.path.join(target_folder, f) for f in os.listdir(target_folder) if f.endswith(('jpg', 'jpeg', 'png'))]
    if not image_files:
        print("Folder poses kosong atau tidak ada file gambar.")
        return

    selected_image_path = None
    animation_start_time = time.time()
    animation_duration = 5  # Durasi animasi (detik)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Animasi acak gambar selama 5 detik pertama
        current_time = time.time()
        if current_time - animation_start_time < animation_duration:
            random_image_path = random.choice(image_files)
            target_image = cv2.imread(random_image_path)
            selected_image_path = random_image_path  # Tetapkan gambar terakhir setelah animasi selesai
        elif selected_image_path:
            target_image = cv2.imread(selected_image_path)

        if target_image is not None:
            target_image_resized = cv2.resize(target_image, (200, 200))

        # Proses face mesh untuk pengguna
        face_results = face_mesh.process(frame_rgb)
        user_features = []

        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                user_feature = {}
                landmarks = face_landmarks.landmark

                # Jarak mata
                left_eye_top = landmarks[386]
                left_eye_bottom = landmarks[374]
                right_eye_top = landmarks[159]
                right_eye_bottom = landmarks[145]

                user_feature['left_eye'] = euclidean_distance(
                    (left_eye_top.x, left_eye_top.y),
                    (left_eye_bottom.x, left_eye_bottom.y)
                )
                user_feature['right_eye'] = euclidean_distance(
                    (right_eye_top.x, right_eye_top.y),
                    (right_eye_bottom.x, right_eye_bottom.y)
                )

                # Jarak mulut
                upper_lip = landmarks[13]
                lower_lip = landmarks[14]
                user_feature['mouth'] = euclidean_distance(
                    (upper_lip.x, upper_lip.y),
                    (lower_lip.x, lower_lip.y)
                )

                user_features.append(user_feature)

        # Bandingkan fitur pengguna dengan target
        if user_features and selected_image_path:
            match = compare_features(user_features, target_features[0])
            if match:
                cv2.putText(frame, "Pose Matched!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Pose Not Matched!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Tempelkan gambar target di pojok kanan atas
        if target_image is not None:
            h, w, _ = frame.shape
            frame[0:200, w-200:w] = target_image_resized

        cv2.imshow("Pose Matching", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
