FROM python:3
WORKDIR /app
ADD . .
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]