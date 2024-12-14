import cv2
import mediapipe as mp
import random
import os
# Menonaktifkan log TensorFlow dan Mediapipe
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # '2' hanya menampilkan error, '3' untuk sepenuhnya menonaktifkan log


# Inisialisasi Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Fungsi untuk membandingkan pose pengguna dengan pose target
def compare_poses(user_landmarks, target_landmarks):
    if not user_landmarks or not target_landmarks:
        return False
    
    # Ambil hanya beberapa landmark kunci (misalnya: bahu, siku, lutut)
    key_indices = [11, 12, 13, 14, 23, 24]  # Contoh: bahu, siku, pinggul, lutut
    threshold = 0.1  # Toleransi perbedaan posisi
    
    for idx in key_indices:
        user_point = user_landmarks[idx]
        target_point = target_landmarks[idx]
        if abs(user_point.x - target_point.x) > threshold or abs(user_point.y - target_point.y) > threshold:
            return False
    return True

# Fungsi utama
def random_pose_filter(target_folder):
    # Pastikan folder target ada
    if not os.path.exists(target_folder):
        print(f"Folder {target_folder} tidak ditemukan!")
        return
    
    # Ambil semua file gambar di folder target
    target_images = [os.path.join(target_folder, f) for f in os.listdir(target_folder) if f.endswith(('.png', '.jpg'))]
    if not target_images:
        print("Tidak ada gambar target ditemukan di folder!")
        return

    # Pilih gambar acak
    target_image_path = random.choice(target_images)
    target_image = cv2.imread(target_image_path)

    if target_image is None:
        print(f"Gagal membaca gambar: {target_image_path}")
        return

    target_image = cv2.resize(target_image, (640, 480))

    # Tampilkan kamera
    cap = cv2.VideoCapture(0)

    # Looping utama
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Gagal membuka kamera!")
            break

        # Flip frame agar seperti cermin
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Deteksi pose pengguna
        result = pose.process(frame_rgb)
        user_landmarks = result.pose_landmarks.landmark if result.pose_landmarks else None

        # Tampilkan gambar target di sudut atas layar
        frame[0:480, 0:640] = target_image

        # Gambar pose pengguna
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Bandingkan pose
        if compare_poses(user_landmarks, result.pose_landmarks.landmark if result.pose_landmarks else None):
            cv2.putText(frame, "Match!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Tampilkan frame
        cv2.imshow("Random Pose Filter", frame)

        # Break jika pengguna menekan 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Jalankan program dengan path folder gambar
images_folder = r"D:\Dingko\TUBES-MULTIMEDIA-IF4021\images"
random_pose_filter(images_folder)
