FROM python:3.9-alpine

WORKDIR /api-test

RUN apk add --no-cache gcc musl-dev linux-headers openssl

COPY requeriments.txt requeriments.txt

RUN pip install --upgrade pip && pip install -r requeriments.txt

# Genera un certificado autofirmado en el directorio /api-test
RUN openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost"

# Expón los puertos necesarios (puerto HTTP y HTTPS)
EXPOSE 8000
EXPOSE 8443

COPY . .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "key.pem", "--ssl-certfile", "cert.pem"]
