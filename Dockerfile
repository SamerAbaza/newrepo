# syntax=docker/dockerfile:experimental
FROM python:3.8-slim
ARG CODE_SOURCE
ARG PACKAGES=""

RUN apt-get update && apt-get --yes upgrade
RUN apt-get --yes install dumb-init bash ${PACKAGES}

RUN mkdir /home/rajendra
WORKDIR /home/rajendra

COPY /${CODE_SOURCE}/requirements_docker.txt /home/rajendra

RUN --mount=type=ssh \
  --mount=type=bind,source=shared_code,target=/shared_code \
  mkdir -p -m 0600 ~/.ssh \
  && apt-get --yes install openssh-client git gcc python3-dev \
  && ssh-keyscan github.com >> ~/.ssh/known_hosts \
  && pip install -r requirements_docker.txt \
  && apt-get --yes remove git openssh-client gcc python3-dev

COPY /${CODE_SOURCE}/src /home/rajendra/

ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["bash", "-c", "sleep 20 && exec python -u main.py"]
# HEALTHCHECK CMD curl -f 127.0.0.1:8080/health || exit 1
