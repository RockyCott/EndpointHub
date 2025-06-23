# ----------------------------------------------------------------------
# 1. Imagen base: slim (sin CUDA) con Python 3.10
#    ‑ puedes cambiar a «python:3.11-slim-bookworm» si prefieres 3.11
# ----------------------------------------------------------------------
FROM python:3.10-slim-bookworm

# Evita prompts en apt y asegura logs in‑order
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Carpeta de trabajo
WORKDIR /app

# ----------------------------------------------------------------------
# 2. Dependencias del sistema
# ----------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------------------------
# 3. Copiar requirements antes (para aprovechar la cache de capas)
# ----------------------------------------------------------------------
COPY requirements.txt .

# ----------------------------------------------------------------------
# 4. Instalar dependencias de Python *sin* cache
#    4.1 Primero pip & lo que venga en requirements.txt
#    4.2 Después PyTorch y torchvision CPU‑only
# ----------------------------------------------------------------------
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    \
    # instalar explícitamente la versión CPU‑only de PyTorch 2.7.1
    # y torchvision 0.22.1 (compatible con PyTorch 2.7.1)
    # (el --index-url apunta al índice de wheels sin CUDA)
    && pip install --no-cache-dir \
        torch==2.7.1 \
        torchvision==0.22.1 \
        --index-url https://download.pytorch.org/whl/cpu

# Si torch/torchvision YA están listados en requirements.txt, elimínalos
# de allí para evitar que pip intente reinstalarlos desde el índice
# público y termine bajando la versión con CUDA.

# ----------------------------------------------------------------------
# 5. Copiar el resto del código fuente
# ----------------------------------------------------------------------
COPY . .

# ----------------------------------------------------------------------
# 6. Descargas en «build time» (solo si es esencial para prod)
# ----------------------------------------------------------------------
RUN python -c "import nltk; nltk.download('stopwords')"


# ----------------------------------------------------------------------
# 7. Exponer el puerto de la app y comando por defecto
# ----------------------------------------------------------------------
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]