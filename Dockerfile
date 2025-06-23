# ----------------------------------------------------------------------
# 1. Base image: slim (no CUDA) with Python 3.10
#    ‑ you can change to `python:3.11-slim-bookworm` if preferred
# ----------------------------------------------------------------------
FROM python:3.10-slim-bookworm

# Avoid apt prompts and ensure log output is ordered
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# ----------------------------------------------------------------------
# 2. System dependencies
# ----------------------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------------------------
# 3. Copy requirements early to leverage Docker layer caching
# ----------------------------------------------------------------------
COPY requirements.txt .

# ----------------------------------------------------------------------
# 4. Install Python dependencies without cache
#    4.1 First pip & requirements.txt
#    4.2 Then explicitly install CPU-only PyTorch and torchvision
# ----------------------------------------------------------------------
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    \
    # explicitly install CPU-only version of PyTorch 2.7.1
    # and torchvision 0.22.1 (compatible with PyTorch 2.7.1)
    # (--index-url points to the no-CUDA wheel index)
    && pip install --no-cache-dir \
        torch==2.7.1 \
        torchvision==0.22.1 \
        --index-url https://download.pytorch.org/whl/cpu

# ----------------------------------------------------------------------
# 5. Copy the rest of the source code
# ----------------------------------------------------------------------
COPY . .

# ----------------------------------------------------------------------
# 6. Build-time downloads
# ----------------------------------------------------------------------
RUN python -c "import nltk; nltk.download('stopwords')"

# ----------------------------------------------------------------------
# 7. Expose app port and set default command
# ----------------------------------------------------------------------
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]    