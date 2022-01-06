FROM continuumio/anaconda3
#FROM python:3.8-slim-buster

WORKDIR /server

SHELL [ "/bin/bash", "--login", "-c" ]


COPY requirements.txt /server/requirements.txt
COPY database.py ./

# Create the environment:
RUN conda create --name eml_server_env

RUN conda init bash
# Activate the environment, and make sure it's activated:
RUN conda activate eml_server_env

RUN pip install -r requirements.txt

RUN echo "conda activate eml_server_env" > ~/.bashrc

COPY . .

EXPOSE 5000

CMD ["python","server.py"]
