FROM debian:bullseye-slim
RUN apt-get -q update \
        && apt-get install -q -y --no-install-recommends \
                zip \
                unzip \
                wget \
                python-dev \
                python3.10 \
		whois \
		telnet \
		python3-pip \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

WORKDIR ${dir}
COPY controller.py functions.py ${dir}
COPY templates/ templates/
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

ENTRYPOINT ["python3","-u","controller.py"]
