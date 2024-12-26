import cv2
import mediapipe as mp
import pickle
import os

# Inisialisasi Mediapipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Fungsi untuk menghitung jarak Euclidean
def euclidean_distance(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

# Fungsi untuk ekstraksi fitur dari landmarks
def extract_features(landmarks):
    if not landmarks:
        return None

    features = {}

    # Jarak mata
    left_eye_top = landmarks[386]
    left_eye_bottom = landmarks[374]
    right_eye_top = landmarks[159]
    right_eye_bottom = landmarks[145]

    features['left_eye'] = euclidean_distance((left_eye_top.x, left_eye_top.y), (left_eye_bottom.x, left_eye_bottom.y))
    features['right_eye'] = euclidean_distance((right_eye_top.x, right_eye_top.y), (right_eye_bottom.x, right_eye_bottom.y))

    # Jarak mulut
    upper_lip = landmarks[13]
    lower_lip = landmarks[14]

    features['mouth'] = euclidean_distance((upper_lip.x, upper_lip.y), (lower_lip.x, lower_lip.y))

    return features

# Fungsi untuk menyimpan fitur target ke file
def save_target_features(target_folder):
    if not os.path.exists(target_folder):
        print(f"Folder {target_folder} tidak ditemukan!")
        return

    target_features = []
    image_files = [f for f in os.listdir(target_folder) if f.endswith(('jpg', 'jpeg', 'png'))]

    for image_file in image_files:
        image_path = os.path.join(target_folder, image_file)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Gagal membaca gambar: {image_path}")
            continue

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_results = face_mesh.process(image_rgb)

        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                features = extract_features(face_landmarks.landmark)
                if features:
                    target_features.append(features)

    if target_features:
        with open("features.pkl", "wb") as f:
            pickle.dump(target_features, f)
        print(f"Fitur berhasil disimpan ke features.pkl")
    else:
        print("Tidak ada fitur yang disimpan. Pastikan gambar memiliki wajah yang terdeteksi.")

# Jalankan proses penyimpanan
if __name__ == "__main__":
    target_folder = os.path.join(os.getcwd() ,'poses')
    save_target_features(target_folder)
