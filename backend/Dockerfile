FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy knowledge base (it's in root/ecomet_reference_full.txt, need to ensure build context allows this)
# Assuming build context is root project dir
COPY ../ecomet_reference_full.txt .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
