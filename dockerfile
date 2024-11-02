FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Expose le port utilisé par Streamlit
EXPOSE 8000

# Lance l'application Streamlit
CMD ["streamlit", "run", "application.py", "--server.port=8000", "--server.enableCORS=false"]
