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
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /home/merks/Prakse/web/Flask-docker
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py --no-check-certificate -O /home/merks/Prakse/web/Flask-docker/get-pip.py
RUN python /home/merks/Prakse/web/Flask-docker/get-pip.py \
	&& pip install Flask

ENTRYPOINT ["python","controller.py"]
