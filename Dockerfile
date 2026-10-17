FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && python -m pip uninstall -y pip

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]