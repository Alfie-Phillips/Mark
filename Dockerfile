FROM python:3
WORKDIR /app
ADD . .
RUN pip3 install --upgrade -r requirements.txt
CMD ["python3", "-u", "main.py"]