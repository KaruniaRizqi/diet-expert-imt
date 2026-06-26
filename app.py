from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import hashlib
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(24)

# ─ DB CONFIG ─ ganti sesuai environment
DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": os.environ.get("MYSQL_DATABASE", "diet_expert_db"),
}


def get_db():
    return mysql.connector.connect(**DB_CONFIG)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ── AUTH DECORATORS ───────────────────────────────────────────────────────────
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Silakan login terlebih dahulu.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        if session.get("role") != "admin":
            flash(
                "Akses ditolak. Hanya Admin yang dapat mengakses halaman ini.", "danger"
            )
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)

    return decorated


# ── IMT LOGIC ─────────────────────────────────────────────────────────────────
def hitung_imt(berat_kg, tinggi_cm):
    tinggi_m = tinggi_cm / 100
    return round(berat_kg / (tinggi_m**2), 2)


def kategori_imt(imt):
    if imt < 17.0:
        return "Kurus"
    elif imt < 18.5:
        return "Kurus"
    elif imt < 25.0:
        return "Normal"
    elif imt < 27.0:
        return "Overweight"
    elif imt < 30.0:
        return "Obesitas I"
    else:
        return "Obesitas II"


def get_rekomendasi(kategori, aktivitas, db):
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM basis_pengetahuan WHERE kategori_imt=%s AND aktivitas=%s LIMIT 1",
        (kategori, aktivitas),
    )
    result = cursor.fetchone()
    cursor.close()
    return result


# ── ROUTES: AUTH ──────────────────────────────────────────────────────────────
@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Username dan password wajib diisi.", "danger")
            return render_template("login.html")
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user WHERE username=%s AND password=%s",
            (username, hash_password(password)),
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()
        if user:
            session["user_id"] = user["id_user"]
            session["username"] = user["username"]
            session["nama"] = user["nama"]
            session["role"] = user["role"]
            flash(f"Selamat datang, {user['nama']}!", "success")
            return redirect(
                url_for("admin_dashboard")
                if user["role"] == "admin"
                else url_for("dashboard")
            )
        flash("Username atau password salah.", "danger")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nama = request.form.get("nama", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        konfirmasi = request.form.get("konfirmasi", "")
        if not all([nama, username, password, konfirmasi]):
            flash("Semua field wajib diisi.", "danger")
            return render_template("register.html")
        if password != konfirmasi:
            flash("Password tidak cocok.", "danger")
            return render_template("register.html")
        if len(password) < 6:
            flash("Password minimal 6 karakter.", "danger")
            return render_template("register.html")
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT id_user FROM user WHERE username=%s", (username,))
        if cursor.fetchone():
            flash("Username sudah digunakan.", "danger")
            cursor.close()
            db.close()
            return render_template("register.html")
        cursor.execute(
            "INSERT INTO user (nama, username, password, role) VALUES (%s,%s,%s,'user')",
            (nama, username, hash_password(password)),
        )
        db.commit()
        cursor.close()
        db.close()
        flash("Akun berhasil dibuat. Silakan login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Anda telah logout.", "info")
    return redirect(url_for("login"))


# ── ROUTES: USER ──────────────────────────────────────────────────────────────
@app.route("/dashboard")
@login_required
def dashboard():
    if session.get("role") == "admin":
        return redirect(url_for("admin_dashboard"))
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM konsultasi WHERE id_user=%s ORDER BY tanggal_konsultasi DESC LIMIT 3",
        (session["user_id"],),
    )
    riwayat = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("dashboard.html", riwayat=riwayat)


@app.route("/konsultasi", methods=["GET", "POST"])
@login_required
def konsultasi():
    if request.method == "POST":
        try:
            berat = float(request.form["berat_badan"])
            tinggi = float(request.form["tinggi_badan"])
            usia = int(request.form["usia"])
            aktivitas = request.form["aktivitas"]
        except (ValueError, KeyError):
            flash(
                "Input tidak valid. Pastikan semua field terisi dengan benar.", "danger"
            )
            return render_template("konsultasi.html")

        if not (1 <= berat <= 300 and 50 <= tinggi <= 250 and 18 <= usia <= 60):
            flash("Data fisik di luar rentang yang valid.", "danger")
            return render_template("konsultasi.html")

        imt = hitung_imt(berat, tinggi)
        kategori = kategori_imt(imt)

        db = get_db()
        # simpan data fisik
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO data_fisik (id_user, berat_badan, tinggi_badan, usia, aktivitas) VALUES (%s,%s,%s,%s,%s)",
            (session["user_id"], berat, tinggi, usia, aktivitas),
        )
        db.commit()

        # ambil rekomendasi
        rekomen = get_rekomendasi(kategori, aktivitas, db)

        if rekomen:
            diet = rekomen["rekomendasi_diet"]
            kalori = rekomen["target_kalori"]
        else:
            diet = "Konsultasikan dengan ahli gizi untuk rekomendasi lebih lanjut."
            kalori = 0

        # simpan ke riwayat konsultasi
        cursor.execute(
            """INSERT INTO konsultasi (id_user, nilai_imt, status_gizi, rekomendasi_diet, target_kalori, tanggal_konsultasi)
               VALUES (%s,%s,%s,%s,%s,%s)""",
            (session["user_id"], imt, kategori, diet, kalori, datetime.now()),
        )
        db.commit()
        cursor.close()
        db.close()

        return render_template(
            "hasil.html",
            imt=imt,
            kategori=kategori,
            aktivitas=aktivitas,
            diet=diet,
            kalori=kalori,
            berat=berat,
            tinggi=tinggi,
        )
    return render_template("konsultasi.html")


@app.route("/riwayat")
@login_required
def riwayat():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM konsultasi WHERE id_user=%s ORDER BY tanggal_konsultasi DESC",
        (session["user_id"],),
    )
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("riwayat.html", riwayat=data)


# ── ROUTES: ADMIN ─────────────────────────────────────────────────────────────
@app.route("/admin")
@admin_required
def admin_dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM user WHERE role='user'")
    total_user = cursor.fetchone()["total"]
    cursor.execute("SELECT COUNT(*) as total FROM konsultasi")
    total_konsultasi = cursor.fetchone()["total"]
    cursor.execute("SELECT COUNT(*) as total FROM basis_pengetahuan")
    total_rules = cursor.fetchone()["total"]
    cursor.execute(
        """SELECT k.*, u.nama FROM konsultasi k 
           JOIN user u ON k.id_user=u.id_user 
           ORDER BY tanggal_konsultasi DESC LIMIT 5"""
    )
    recent = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template(
        "admin_dashboard.html",
        total_user=total_user,
        total_konsultasi=total_konsultasi,
        total_rules=total_rules,
        recent=recent,
    )


@app.route("/admin/basis-pengetahuan")
@admin_required
def admin_basis():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM basis_pengetahuan ORDER BY kategori_imt, aktivitas")
    rules = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("admin_basis.html", rules=rules)


@app.route("/admin/basis-pengetahuan/tambah", methods=["GET", "POST"])
@admin_required
def admin_tambah_rule():
    if request.method == "POST":
        try:
            kategori = request.form["kategori_imt"]
            aktivitas = request.form["aktivitas"]
            diet = request.form["rekomendasi_diet"].strip()
            kalori = int(request.form["target_kalori"])
        except (ValueError, KeyError):
            flash("Semua field wajib diisi dengan benar.", "danger")
            return render_template("admin_form_rule.html", rule=None, action="Tambah")
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO basis_pengetahuan (kategori_imt, aktivitas, rekomendasi_diet, target_kalori) VALUES (%s,%s,%s,%s)",
            (kategori, aktivitas, diet, kalori),
        )
        db.commit()
        cursor.close()
        db.close()
        flash("Aturan berhasil ditambahkan.", "success")
        return redirect(url_for("admin_basis"))
    return render_template("admin_form_rule.html", rule=None, action="Tambah")


@app.route("/admin/basis-pengetahuan/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def admin_edit_rule(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    if request.method == "POST":
        try:
            kategori = request.form["kategori_imt"]
            aktivitas = request.form["aktivitas"]
            diet = request.form["rekomendasi_diet"].strip()
            kalori = int(request.form["target_kalori"])
        except (ValueError, KeyError):
            flash("Semua field wajib diisi dengan benar.", "danger")
            cursor.execute("SELECT * FROM basis_pengetahuan WHERE id_rule=%s", (id,))
            rule = cursor.fetchone()
            cursor.close()
            db.close()
            return render_template("admin_form_rule.html", rule=rule, action="Edit")
        cursor2 = db.cursor()
        cursor2.execute(
            "UPDATE basis_pengetahuan SET kategori_imt=%s, aktivitas=%s, rekomendasi_diet=%s, target_kalori=%s WHERE id_rule=%s",
            (kategori, aktivitas, diet, kalori, id),
        )
        db.commit()
        cursor2.close()
        cursor.close()
        db.close()
        flash("Aturan berhasil diperbarui.", "success")
        return redirect(url_for("admin_basis"))
    cursor.execute("SELECT * FROM basis_pengetahuan WHERE id_rule=%s", (id,))
    rule = cursor.fetchone()
    cursor.close()
    db.close()
    if not rule:
        flash("Aturan tidak ditemukan.", "danger")
        return redirect(url_for("admin_basis"))
    return render_template("admin_form_rule.html", rule=rule, action="Edit")


@app.route("/admin/basis-pengetahuan/hapus/<int:id>", methods=["POST"])
@admin_required
def admin_hapus_rule(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM basis_pengetahuan WHERE id_rule=%s", (id,))
    db.commit()
    cursor.close()
    db.close()
    flash("Aturan berhasil dihapus.", "success")
    return redirect(url_for("admin_basis"))


@app.route("/admin/riwayat")
@admin_required
def admin_riwayat():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """SELECT k.*, u.nama, u.username FROM konsultasi k 
           JOIN user u ON k.id_user=u.id_user 
           ORDER BY tanggal_konsultasi DESC"""
    )
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("admin_riwayat.html", riwayat=data)


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
