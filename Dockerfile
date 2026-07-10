Imagen base: Python 3 en variante "slim" (ligera). Fijamos la versión menor
3.12 porque con la etiqueta genérica python:3-slim (hoy Python 3.14) la
librería psycopg2 no dispone de paquete precompilado y falla la construcción.
FROM python:3.12-slim

Carpeta de trabajo dentro del contenedor
WORKDIR /aplicacion

1) Copiamos SOLO el requirements y lo instalamos
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

2) Recién ahora copiamos el resto del código
COPY app/ .

Puerto interno donde escucha Flask
EXPOSE 5000

Comando que arranca la aplicación
CMD ["python", "app.py"]