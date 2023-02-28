FROM python:3.9-alpine

WORKDIR /api-test

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requeriments.txt requeriments.txt

RUN pip install --upgrade pip

RUN pip install -r requeriments.txt

COPY . .

CMD ["uvicorn","main:app","--reload","--host","0.0.0.0","--port","8000"]
