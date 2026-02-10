FROM python:3.9

WORKDIR /backend

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# optional: only if you want the image to run even without bind mount
COPY ./src /backend/src

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/backend/src"]
