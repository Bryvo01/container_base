FROM python:alpine3.16
WORKDIR /usr/app/src
COPY dynamic_godaddy.py ./
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
CMD ["python3", "./dynamic_godaddy.py"]
