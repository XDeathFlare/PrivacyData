from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="botakbermantel7!",
        database="db_mahasiswa"
    )


@app.route("/")
def home():
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM mahasiswa")
        total_mahasiswa = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM dosen")
        total_dosen = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM mata_kuliah")
        total_mata_kuliah = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM krs")
        total_krs = cursor.fetchone()[0]

        return render_template(
            "index.html",
            total_mahasiswa=total_mahasiswa,
            total_dosen=total_dosen,
            total_mata_kuliah=total_mata_kuliah,
            total_krs=total_krs
        )

    except Error as e:
        return f"Koneksi database gagal: {e}", 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None and conn.is_connected():
            conn.close()

@app.route("/mahasiswa")
def daftar_mahasiswa():
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT nim, nama, program_studi, no_absen
            FROM mahasiswa
            ORDER BY nim
        """)

        data_mahasiswa = cursor.fetchall()

        return render_template(
            "mahasiswa.html",
            data_mahasiswa=data_mahasiswa
        )

    except Error as e:
        return f"Gagal mengambil data mahasiswa: {e}", 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None and conn.is_connected():
            conn.close()

@app.route("/dosen")
def daftar_dosen():
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_dosen, nama_dosen, program_studi, email
            FROM dosen
            ORDER BY id_dosen
        """)

        data_dosen = cursor.fetchall()

        return render_template(
            "dosen.html",
            data_dosen=data_dosen
        )

    except Error as e:
        return f"Gagal mengambil data dosen: {e}", 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None and conn.is_connected():
            conn.close()

@app.route("/matakuliah")
def daftar_mata_kuliah():
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                kode_mk,
                nama_mata_kuliah,
                program_studi,
                sks,
                id_dosen
            FROM mata_kuliah
            ORDER BY kode_mk
        """)

        data_mata_kuliah = cursor.fetchall()

        return render_template(
            "matakuliah.html",
            data_mata_kuliah=data_mata_kuliah
        )

    except Error as e:
        return f"Gagal mengambil data mata kuliah: {e}", 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None and conn.is_connected():
            conn.close()

@app.route("/krs")
def daftar_krs():
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                k.id_krs,
                k.nim,
                m.nama AS nama_mahasiswa,
                k.kode_mk,
                mk.nama_mata_kuliah,
                k.semester,
                k.tahun_ajaran
            FROM krs AS k
            LEFT JOIN mahasiswa AS m
                ON k.nim = m.nim
            LEFT JOIN mata_kuliah AS mk
                ON k.kode_mk = mk.kode_mk
            ORDER BY k.id_krs
        """)

        data_krs = cursor.fetchall()

        return render_template(
            "krs.html",
            data_krs=data_krs
        )

    except Error as e:
        return f"Gagal mengambil data KRS: {e}", 500

    finally:
        if cursor is not None:
            cursor.close()

        if conn is not None and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    app.run(debug=True)