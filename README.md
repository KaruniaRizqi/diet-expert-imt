# DietExpert IMT — Sistem Pakar Penentuan Pola Diet Sehat
Kelompok 3 | Expert System | Informatika UST 2026

## Stack
- **Backend**: Python 3.10+ / Flask
- **Database**: MySQL
- **Frontend**: Jinja2 + Pure CSS (medical modern UI)

---

## Setup & Instalasi

### 1. Clone / Ekstrak Project
```
diet_expert/
├── app.py
├── requirements.txt
├── schema.sql
├── static/css/style.css
└── templates/
    ├── base.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── konsultasi.html
    ├── hasil.html
    ├── riwayat.html
    ├── admin_dashboard.html
    ├── admin_basis.html
    ├── admin_form_rule.html
    └── admin_riwayat.html
```

### 2. Buat Virtual Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database MySQL
Buka MySQL/phpMyAdmin, lalu jalankan file `schema.sql`:
```bash
mysql -u root -p < schema.sql
```
Atau copy-paste isi `schema.sql` ke phpMyAdmin > SQL.

### 5. Konfigurasi Koneksi DB
Edit bagian `DB_CONFIG` di `app.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',        # ganti sesuai MySQL lo
    'password': '',        # ganti sesuai password MySQL lo
    'database': 'diet_expert_db'
}
```

### 6. Jalankan Aplikasi
```bash
python app.py
```
Buka browser: **http://127.0.0.1:5000**

---


## Fitur Sistem

### User
- Registrasi & Login
- Konsultasi IMT (input berat, tinggi, usia, aktivitas)
- Preview estimasi IMT real-time saat input
- Hasil konsultasi lengkap + rekomendasi diet
- Riwayat konsultasi

### Admin
- Dashboard statistik (total user, konsultasi, aturan)
- Kelola Basis Pengetahuan (tambah, edit, hapus aturan IF-THEN)
- Lihat semua riwayat konsultasi seluruh pengguna

---

## Kategori IMT (Kemenkes RI)
| Kategori    | IMT          |
|-------------|--------------|
| Kurus       | < 18.5       |
| Normal      | 18.5 – 24.9  |
| Overweight  | 25.0 – 26.9  |
| Obesitas I  | 27.0 – 29.9  |
| Obesitas II | ≥ 30.0       |

---

## Rumus IMT
```
IMT = Berat Badan (kg) / Tinggi Badan² (m²)
```


