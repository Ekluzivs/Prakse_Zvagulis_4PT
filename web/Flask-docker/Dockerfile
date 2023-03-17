FROM debian:bullseye-slim
RUN apt-get -q update \
        && apt-get install -q -y --no-install-recommends \
                zip \
                unzip \
                wget \
                python-dev \
                python3 \
		whois \
		telnet \
		python3-pip \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /home/merks/Prakse/web/Flask-docker
COPY controller.py function.py /home/merks/Prakse/web/Flask-docker
COPY templates/ templates/
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["python3","controller.py"]
