FROM python:3.9-alpine

WORKDIR /api-test

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requeriments.txt requeriments.txt

RUN pip install --upgrade pip

RUN pip install -r requeriments.txt

# Instala OpenSSL
RUN apk add --no-cache openssl

# Genera un certificado autofirmado en el directorio /ssl
RUN openssl req -x509 -newkey rsa:4096 -nodes -out /ssl/cert.pem -keyout /ssl/key.pem -days 365 -subj "/CN=localhost"

# Expón los puertos necesarios (puerto HTTP y HTTPS)
EXPOSE 8000
EXPOSE 8443

# Copia los certificados desde el directorio /ssl en el contenedor hacia el directorio de trabajo /api-test
COPY --from=builder /ssl/cert.pem /api-test/cert.pem
COPY --from=builder /ssl/key.pem /api-test/key.pem

COPY . .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "key.pem", "--ssl-certfile", "cert.pem"]

