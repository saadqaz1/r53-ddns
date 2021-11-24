FROM python:3.10.0-alpine3.14
WORKDIR /app
ENV TZ=America/New_York
ENV LOG_PATH=/app/
COPY .env .env
COPY pyawsdns.log pyawsdns.log
COPY awsdns.py awsdns.py
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip install awscli
ENTRYPOINT ["python3", "awsdns.py"]