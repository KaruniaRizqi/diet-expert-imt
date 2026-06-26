DietExpert IMT - Sistem Pakar Penentuan Pola Diet Sehat

link: https://diet-expert-imt-production.up.railway.app/

Proyek ini merupakan aplikasi sistem pakar yang digunakan untuk memberikan rekomendasi pola diet berdasarkan nilai Indeks Massa Tubuh (IMT). Aplikasi dibuat menggunakan Flask dengan database MySQL sebagai bagian dari tugas mata kuliah Sistem Pakar.

Teknologi

- Python 3
- Flask
- MySQL
- HTML, CSS (Jinja2)

Cara Menjalankan

1. Clone repository ini.
2. Install dependency.
   pip install -r requirements.txt
3. Import database menggunakan file "schema.sql".
4. Sesuaikan konfigurasi database pada file "app.py".
5. Jalankan aplikasi.
   python app.py
6. Buka browser dan akses:
   http://127.0.0.1:5000


Fitur

User

- Registrasi dan login.
- Melakukan konsultasi IMT.
- Melihat hasil konsultasi beserta rekomendasi pola diet.
- Melihat riwayat konsultasi.

Admin

- Melihat dashboard.
- Mengelola basis pengetahuan (tambah, ubah, dan hapus aturan).
- Melihat riwayat konsultasi seluruh pengguna.

Rumus IMT

IMT = Berat Badan (kg) / Tinggi Badan² (m²)

Catatan: Aplikasi ini dibuat untuk tujuan edukasi dan pembelajaran, sehingga hasil yang diberikan bukan merupakan diagnosis medis.
