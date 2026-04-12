# Stage 1: Build (dependency instalation)
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
# Instalamos dependencias en un directorio local
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final (light image for exec)
FROM python:3.11-slim

WORKDIR /app
# Copiamos solo las dependencias instaladas y el código
COPY --from=builder /root/.local /root/.local
COPY . .

# Asegurar que el PATH incluya las librerías instaladas
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000
CMD ["python", "app.py"]