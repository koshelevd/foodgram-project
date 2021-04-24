FROM python:3.7.4
WORKDIR /code
COPY . /code
RUN pip install -r requirements.txt
COPY prepare.sh /prepare.sh
RUN chmod +x /prepare.sh