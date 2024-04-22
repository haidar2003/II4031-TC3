# II4031-TC2
 Tugas 3 II4031 Kriptografi dan Koding Semester II Tahun 2023/2024
 # Dibuat Oleh
 Muhammad Rafi Haidar - 18221134
 Raditya Azka Prabaswara - 18221152
# Deskripsi
Program ini bertujuan untuk melakukan enkripsi dan dekripsi asimetris pada teks maupun berkas. Program ini menggunakan algoritma RSA.
# Batasan
- Python 3.12 atau terbaru
- Untuk enkripsi teks maupun enkripsi berkas teks (.txt) hanya dapat mengandung karakter yang terdapat pada "latin1"
- Ukuran berkas input sebaiknya berukuran lebih kecil dari 10 KB
# Fitur
Dapat mengenkripsi masukan teks dan berkas sembarang dengan RSA.
# Petunjuk Penggunaan
1. Unduh berkas Zip kode sumber dari repository atau clone repository Github
2. Buka direktori yang sudah berisi kode sumber melalui CLI seperti terminal atau command prompt, atau buka direktori kode sumber di aplikasi IDE seperti Visual Studio Code
3. Unduh semua package python yang digunakan di program ini, apabila ingin menggunakan intrepeter yang terdapat di virtual environment yang disediakan, ketik pada command prompt
   >  pip install -r requirements.txt  
4. Jalankan berkas gui.py, apabila menggunakan command prompt, ketik
   >  python gui.py  
5. Tekan tombol Generate Key pada kedua user  
6. Tekan tombol Send Key pada kedua user  
7. Pilih input type pada user pengirim  
8. Tuliskan teks pada input pengirim untuk teks  
atau untuk file, tekan tombol upload user pengirim, dan pilih file yang akan dikirim  
9. Tekan tombol Encrypt and Send  
10. Pesan akan muncul pada bagian user penerima dengan sudah terenkripsi dan dengan encoding base64  
11. (Opsional) Gunakan tombol save di bagian bawah layar untuk mengunduh pesan sesuai dengan tulisan yang tertera pada tombol  
