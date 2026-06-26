-- ============================================================
--  SISTEM PAKAR DIET SEHAT BERDASARKAN IMT
--  Database: diet_expert_db
-- ============================================================

CREATE DATABASE IF NOT EXISTS diet_expert_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE diet_expert_db;

-- ── TABEL USER ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user (
    id_user     INT AUTO_INCREMENT PRIMARY KEY,
    nama        VARCHAR(100) NOT NULL,
    username    VARCHAR(50) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        ENUM('user','admin') NOT NULL DEFAULT 'user',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ── TABEL DATA FISIK ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS data_fisik (
    id_data      INT AUTO_INCREMENT PRIMARY KEY,
    id_user      INT NOT NULL,
    berat_badan  FLOAT NOT NULL,
    tinggi_badan FLOAT NOT NULL,
    usia         INT NOT NULL,
    aktivitas    ENUM('Sedentari','Ringan','Sedang','Berat') NOT NULL,
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES user(id_user) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ── TABEL BASIS PENGETAHUAN ──────────────────────────────────
CREATE TABLE IF NOT EXISTS basis_pengetahuan (
    id_rule           INT AUTO_INCREMENT PRIMARY KEY,
    kategori_imt      VARCHAR(20) NOT NULL,
    aktivitas         VARCHAR(20) NOT NULL,
    rekomendasi_diet  TEXT NOT NULL,
    target_kalori     INT NOT NULL
) ENGINE=InnoDB;

-- ── TABEL KONSULTASI ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS konsultasi (
    id_konsultasi       INT AUTO_INCREMENT PRIMARY KEY,
    id_user             INT NOT NULL,
    nilai_imt           FLOAT NOT NULL,
    status_gizi         VARCHAR(20) NOT NULL,
    rekomendasi_diet    TEXT NOT NULL,
    target_kalori       INT NOT NULL,
    tanggal_konsultasi  DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES user(id_user) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
--  SEED: AKUN DEFAULT
--  password admin   = admin123  (sha256)
--  password demo    = user123   (sha256)
-- ============================================================
INSERT INTO user (nama, username, password, role) VALUES
('Administrator', 'admin',
 '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a3', 'admin'),
('Demo User', 'demo',
 '8c27ef5988e2f24de786a4fd06e2baa30fb08c77a23cd5a4b5d7d22c71e4fce0', 'user');

-- ============================================================
--  SEED: BASIS PENGETAHUAN (20 RULES)
--  Kategori: Kurus | Normal | Overweight | Obesitas I | Obesitas II
--  Aktivitas: Sedentari | Ringan | Sedang | Berat
-- ============================================================
INSERT INTO basis_pengetahuan (kategori_imt, aktivitas, rekomendasi_diet, target_kalori) VALUES

-- KURUS
('Kurus', 'Sedentari',
 'Diet Penambahan Berat Badan: Tingkatkan asupan kalori dengan makanan bergizi seperti nasi, protein hewani, kacang-kacangan, dan lemak sehat. Makan 5–6 kali sehari dengan porsi sedang. Hindari makanan junk food meskipun berkalori tinggi.',
 2200),
('Kurus', 'Ringan',
 'Diet Penambahan Berat Badan Aktif: Konsumsi makanan tinggi protein dan karbohidrat kompleks. Tambahkan camilan sehat antara waktu makan utama seperti roti gandum dengan selai kacang atau yogurt. Pastikan tidur cukup untuk mendukung pembentukan massa tubuh.',
 2400),
('Kurus', 'Sedang',
 'Diet Penambahan Berat Badan dengan Aktivitas Sedang: Penuhi kebutuhan energi dengan memperbanyak sumber karbohidrat kompleks (nasi, kentang, oat) dan protein (daging, telur, tahu, tempe). Konsumsi 3 makanan utama dan 2–3 camilan sehat per hari.',
 2600),
('Kurus', 'Berat',
 'Diet Penambahan Berat Badan Intensif: Butuh asupan kalori dan protein yang lebih tinggi untuk mendukung aktivitas berat. Konsumsi makanan padat nutrisi: daging merah, ikan, telur, nasi, pisang, dan susu penuh lemak. Pertimbangkan suplemen protein jika diperlukan setelah berkonsultasi dengan ahli gizi.',
 3000),

-- NORMAL
('Normal', 'Sedentari',
 'Diet Pemeliharaan Berat Badan: Pertahankan pola makan 3 kali sehari dengan gizi seimbang. Perbanyak sayur dan buah, batasi makanan olahan dan minuman manis. Tingkatkan aktivitas fisik ringan seperti berjalan kaki minimal 30 menit per hari.',
 1900),
('Normal', 'Ringan',
 'Diet Seimbang: Pertahankan komposisi makan yang baik dengan karbohidrat 50–55%, protein 15–20%, dan lemak sehat 25–30%. Minum air putih minimal 8 gelas per hari. Perbanyak variasi sayur dan buah berwarna-warni.',
 2100),
('Normal', 'Sedang',
 'Diet Seimbang Aktif: Konsumsi makanan bergizi seimbang dengan porsi yang disesuaikan aktivitas. Pastikan asupan protein cukup untuk mempertahankan massa otot. Pilih karbohidrat kompleks sebagai sumber energi utama dan hindari minuman berkalori tinggi.',
 2300),
('Normal', 'Berat',
 'Diet Performa: Tingkatkan asupan karbohidrat kompleks dan protein untuk mendukung aktivitas fisik berat. Konsumsi makanan kaya zat besi, magnesium, dan elektrolit. Jangan lewatkan sarapan dan pastikan makan dalam 1–2 jam setelah berolahraga.',
 2700),

-- OVERWEIGHT
('Overweight', 'Sedentari',
 'Diet Penurunan Berat Badan: Kurangi asupan kalori 300–500 kkal dari kebutuhan harian. Batasi karbohidrat sederhana dan makanan berminyak. Perbanyak konsumsi sayuran, protein tanpa lemak (dada ayam, ikan, tahu), dan serat. Mulai dengan aktivitas ringan seperti jalan kaki 20 menit per hari.',
 1500),
('Overweight', 'Ringan',
 'Diet Rendah Kalori: Batasi makanan tinggi gula dan lemak jenuh. Pilih metode memasak yang sehat: rebus, kukus, atau panggang. Konsumsi protein tanpa lemak dan perbanyak sayuran untuk rasa kenyang lebih lama. Tingkatkan durasi aktivitas fisik secara bertahap.',
 1700),
('Overweight', 'Sedang',
 'Diet Rendah Kalori Aktif: Kombinasikan pengurangan kalori dengan aktivitas fisik yang rutin. Prioritaskan protein di setiap waktu makan untuk menjaga massa otot. Hindari makanan ultra-proses dan minuman manis. Catat asupan makanan harian untuk memantau progres.',
 1900),
('Overweight', 'Berat',
 'Diet Seimbang dengan Defisit Kalori Ringan: Meski beraktivitas berat, tetap jaga defisit kalori ringan 200–300 kkal. Penuhi kebutuhan protein tinggi dan karbohidrat kompleks. Hindari makanan gorengan dan olahan. Konsultasikan dengan ahli gizi untuk program yang lebih personal.',
 2100),

-- OBESITAS I
('Obesitas I', 'Sedentari',
 'Diet Penurunan Berat Badan Terkontrol: Kurangi kalori secara bertahap (500 kkal/hari). Hindari gula tambahan, tepung putih, dan makanan gorengan. Perbanyak sayuran hijau, protein tanpa lemak, dan minum air putih sebelum makan. Sangat disarankan berkonsultasi dengan dokter atau ahli gizi.',
 1300),
('Obesitas I', 'Ringan',
 'Diet Rendah Kalori Terstruktur: Batasi makanan tinggi kalori dan fokus pada makanan volume tinggi namun kalori rendah (sayuran, sup bening, buah rendah gula). Jaga asupan protein untuk mencegah kehilangan massa otot. Mulai dengan olahraga ringan secara konsisten.',
 1500),
('Obesitas I', 'Sedang',
 'Diet Penurunan Berat Badan Aktif: Kombinasikan pola makan rendah kalori dengan olahraga aerobik. Kurangi porsi nasi, ganti dengan karbohidrat kompleks seperti ubi atau oat. Tingkatkan asupan protein dan sayuran. Pantau berat badan secara berkala.',
 1700),
('Obesitas I', 'Berat',
 'Diet Kontrol Kalori dengan Aktivitas Tinggi: Meski aktif secara fisik, tetap perlu defisit kalori. Fokus pada makanan padat nutrisi. Jaga keseimbangan elektrolit dan hidrasi yang baik. Wajib berkonsultasi dengan tenaga kesehatan untuk panduan lebih lanjut.',
 1900),

-- OBESITAS II
('Obesitas II', 'Sedentari',
 'Diet Medis Intensif: Kondisi ini memerlukan pendampingan tenaga medis. Secara umum: kurangi kalori signifikan, hindari total makanan tinggi gula dan lemak jenuh, perbanyak sayuran non-tepung, protein tanpa lemak, dan minum air putih. WAJIB berkonsultasi dengan dokter dan ahli gizi sebelum memulai program diet apapun.',
 1200),
('Obesitas II', 'Ringan',
 'Diet Medis Terpandu: Segera konsultasikan dengan dokter dan ahli gizi. Program diet harus disesuaikan dengan kondisi kesehatan secara menyeluruh. Hindari makanan ultra-proses, minuman manis, dan makanan tinggi lemak jenuh. Mulai dengan aktivitas fisik yang aman dan terukur.',
 1400),
('Obesitas II', 'Sedang',
 'Diet Penurunan Berat Badan Intensif: Diperlukan program komprehensif dari tenaga kesehatan. Kurangi asupan kalori secara signifikan dengan tetap memenuhi kebutuhan nutrisi esensial. Pilih makanan tinggi serat, protein tanpa lemak, dan lemak sehat. Aktivitas fisik harus dipantau oleh profesional.',
 1500),
('Obesitas II', 'Berat',
 'Program Kesehatan Komprehensif: Kondisi ini memerlukan evaluasi medis menyeluruh. Aktivitas fisik berat dengan IMT sangat tinggi dapat berisiko tanpa pengawasan medis. SANGAT DISARANKAN berkonsultasi dengan dokter sebelum melanjutkan aktivitas fisik dan memulai program diet apapun.',
 1600);
