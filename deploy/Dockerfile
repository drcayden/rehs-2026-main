# REHS 2026 NRP chatbot image.
# Build from the repo root:  docker build -t rehs-chatbot:v0.1 -f deploy/Dockerfile .
FROM python:3.12-slim

WORKDIR /app

# Install deps first so this layer caches when only source changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code.
COPY src/ ./src/
COPY app.py .
COPY data/chunks/ ./data/chunks/

# TODO(week-07): decide how the vector DB gets into the pod. Options:
#   (a) seed an empty PVC with a one-shot Job that runs scripts/ingest.py + index,
#   (b) an initContainer that ingests on first start, or
#   (c) bake a pre-built chroma_db/ into the image (easiest, largest).
# If you go with (c), COPY it here. Otherwise the PVC mount provides /app/chroma_db.
# COPY data/ ./data/

EXPOSE 8501

# --server.address=0.0.0.0 is REQUIRED inside a container (Streamlit binds localhost
# by default, which is unreachable from outside the container).
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
