FROM python:3.12-slim
RUN groupadd -r soc && useradd -r -g soc soc
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app app
COPY tests tests
COPY detection_rules detection_rules
COPY synthetic_data synthetic_data
USER soc
HEALTHCHECK --interval=30s --timeout=5s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
