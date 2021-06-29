FROM fnndsc/ubuntu-python3

RUN apt-get update \
  && apt-get install -y git

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY main.py main.py

ENTRYPOINT ["python3", "main.py"]

