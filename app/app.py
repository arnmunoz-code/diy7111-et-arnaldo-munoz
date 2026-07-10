import os
import time
import psycopg2
from flask import Flask

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "registro_visitas")
DB_USER = os.environ.get("DB_USER", "amg_user")
DB_PASS = os.environ.get("DB_PASSWORD", "amg_secret")
DB_PORT = os.environ.get("DB_PORT", "5432")


def conectar():
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER,
        password=DB_PASS, port=DB_PORT,
    )


def preparar_tabla():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS registro (id SERIAL PRIMARY KEY, momento TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def inicio():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO registro DEFAULT VALUES;")
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM registro;")
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return (
        "<h1>Plataforma VZeta &mdash; Despliegue de Arnaldo Munoz (AMG)</h1>"
        f"<h2>Visitas registradas: {total}</h2>"
        "<p>Datos almacenados de forma persistente en PostgreSQL.</p>"
    )


if __name__ == "__main__":
    for intento in range(15):
        try:
            preparar_tabla()
            break
        except Exception as error:
            print(f"Base no disponible aun: {error}")
            time.sleep(3)
    app.run(host="0.0.0.0", port=5000)