from flask import Flask
from redis import Redis
import os

app = Flask(__name__)

# Configuración de Redis usando la variable de entorno o el nombre del servicio en Docker
redis_host = os.getenv('REDIS_HOST', 'db')
cache = Redis(host=redis_host, port=6379)

@app.route('/')
def hello():
    try:
        # Incrementamos un contador en Redis cada vez que se visita la página
        visits = cache.incr('hits')
    except Exception:
        visits = "no disponible (Redis no conectado)"
    
    return f"""
    <h1>¡Hola desde Flask en Docker!</h1>
    <p>Esta página ha sido visitada <b>{visits}</b> veces.</p>
    <p>Estado del entorno: <b>Producción (AWS Exercise)</b></p>
    """

if __name__ == "__main__":
    # Importante: host='0.0.0.0' para que sea accesible desde fuera del contenedor
    app.run(host='0.0.0.0', port=5000)