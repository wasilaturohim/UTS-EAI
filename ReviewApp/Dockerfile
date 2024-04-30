# base image
FROM python:3.9-slim

# create working dir
WORKDIR /app

# copy all files
COPY . /app

# Menginstal dependensi
RUN pip install -r requirements.txt

EXPOSE 5003

# Menjalankan aplikasi saat kontainer dimulai
CMD ["python", "review.py"]

