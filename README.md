# TUBES-MULTIMEDIA-IF4021

# Filter Gaya Foto Random  

## Anggota Kelompok  
| **Nama**                     | **NIM**     | **GitHub**               |  
|------------------------------|-------------|--------------------------|  
| Muhamad Rizzky Nopriansyah   | 121140132   | [Mrnopri](#)             |  
| Muhammad Atha Akbar          | 121140123   | [AthaAkbar123](#)        |  
| Gabriel Fico D.              | 121140069   | [gabrielfico](#)         |  

## Deskripsi Proyek  
Proyek ini bertujuan untuk mengembangkan filter gaya foto random menggunakan Python, OpenCV, dan Mediapipe. Filter ini memungkinkan pengguna untuk meniru pose atau gaya yang ditampilkan secara acak di layar secara real-time.  

Dengan bantuan teknologi pose detection dari Mediapipe, aplikasi ini dapat melacak pergerakan tubuh pengguna dan membandingkannya dengan pose target untuk memastikan kesesuaian. Jika gaya yang dilakukan pengguna sesuai dengan pose target, aplikasi akan memberikan umpan balik berupa notifikasi "Pose Matched!" di layar.  

## Fitur Utama  
- **Pose Acak**: Menampilkan pose atau gaya secara acak untuk ditiru pengguna.  
- **Pelacakan Real-Time**: Melacak ekspresi wajah pengguna dengan menggunakan Mediapipe.  
- **Umpan Balik Visual**: Memberikan notifikasi langsung jika pose pengguna sesuai dengan target.  
- **Pengalaman Interaktif**: Antarmuka sederhana dan responsif menggunakan live camera feed.  

## Teknologi yang Digunakan  
- **Python**: Bahasa utama untuk pengembangan aplikasi.  
- **OpenCV**: Untuk pemrosesan video real-time dan menampilkan pose target.  
- **Mediapipe**: Untuk mendeteksi dan melacak pose tubuh secara akurat.  
- **Tensorflow**: Untuk tujuan yang lebih umum dalam pengolahan gambar dan video

## Tujuan Proyek  
Proyek ini bertujuan untuk menciptakan aplikasi interaktif yang menghibur dan bermanfaat.

## Logbook  
| No | Tanggal          | Progress                                |
|----|------------------|-----------------------------------------|
| 1  | 14 Desember 2024 | Update program yang telah dikerjakan            |
| 2  | 17 Desember 2024 | Menentukan Pembagian Tugas              |
| 3  | 20 Desember 2024 | Pembuatan Program beserta format laporan|
| 4  | 23 Desember 2024 | Update program untuk randomize foto dan testing |
| 5  | 24 Desember 2024 | Update final program yang telah diperbaiki                |

## Untuk Penginstallan 
- **Python**: Download Python dari situs resmi python.org dan ikuti petunjuk instalasi.
Setelah instalasi, pastikan Python terinstal dengan menjalankan perintah python --version di terminal atau command prompt.
- **OpenCV** : pip install opencv-python diterminal
- **Mediapipe** : pip install mediapipe
- **Tensorflow** : pip install tensorflow

## Cara Menggunakan Filter
- Jalankan ekstrai fitur dengan yaitu file bernama "feature_extractor.py"
- Kemudian jalankan file utama yaiut file bernama "main.py"

note : jika terjadi error dalam penginstallan `ERROR: Could not install packages due to an OSError: Could not find a suitable TLS CA certificate bundle, invalid path:` bisa mencoba dengan `pip install mediapipe tensorflow --trusted-host pypi.org --trusted-host files.pythonhosted.org`