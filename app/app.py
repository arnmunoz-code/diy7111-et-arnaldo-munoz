import os
import time
import psycopg2
from flask import Flask

app = Flask(name)

--- Datos de conexión leídos desde variables de entorno ---
Nunca se escriben las credenciales "a fuego" en el código.
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "registro_visitas")
DB_USER = os.environ.get("DB_USER", "amg_user")
DB_PASS = os.environ.get("DB_PASSWORD", "amg_secret")
DB_PORT = os.environ.get("DB_PORT", "5432")


def conectar():
    """Devuelve una conexión abierta a PostgreSQL."""
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER,
        password=DB_PASS, port=DB_PORT,
    )


def preparar_tabla():
    """Crea la tabla de visitas la primera vez."""
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS registro (
            id SERIAL PRIMARY KEY,
            momento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def inicio():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO registro DEFAULT VALUES;")   # registra la visita
    conn.commit()
    cur.execute("SELECT COUNT(*) FROM registro;")          # cuenta el total
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return (
        "<h1>Plataforma VZeta &mdash; Despliegue de Arnaldo Muñoz (AMG)</h1>"
        f"<h2>Visitas registradas: {total}</h2>"
        "<p>Datos almacenados de forma persistente en PostgreSQL.</p>"
    )


if name == "main":
    # La base tarda unos segundos en aceptar conexiones al arrancar:
    # reintentamos hasta que esté lista.
    for intento in range(15):
        try:
            preparar_tabla()
            break
        except Exception as error:
            print(f"Base no disponible aún: {error}")
            time.sleep(3)
    app.run(host="0.0.0.0", port=5000)