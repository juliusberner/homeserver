FROM python:3.9

WORKDIR /app
COPY . .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    chmod -R u=rwx,go=rx main.py telegram_status

CMD ["python", "-u", "main.py"]
