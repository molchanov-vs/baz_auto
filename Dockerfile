FROM python:3.11.3
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY urls.txt .
COPY /utils/utils.py .
COPY get_baz_auto.py .
ENTRYPOINT ["python","./get_baz_auto.py"]
