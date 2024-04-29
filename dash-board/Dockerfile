FROM python:3.11

ARG host
ARG port
ENV host=${host} port=${port}

WORKDIR /dashboad

COPY ./dash-board/. .

RUN pip install -r requirements.txt

ENTRYPOINT python app.py --host=$host --port=$port

