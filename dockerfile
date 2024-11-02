FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Expose le port utilisé par Streamlit
EXPOSE 8501

# Lance l'application Streamlit
CMD ["streamlit", "run", "application.py", "--server.port=8501", "--server.enableCORS=false"]