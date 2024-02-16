FROM python:3.10-slim-bookworm as prod

RUN apt update && \
    apt install -y make curl && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

ARG USERNAME=ryeuser
RUN useradd ${USERNAME} --create-home
USER ${USERNAME}
WORKDIR /home/${USERNAME}/highscore-micro-two
COPY --chmod=+w .python-version .python_version

ENV RYE_HOME /home/${USERNAME}/.rye
ENV PATH="${RYE_HOME}/shims:${PATH}"

COPY . .
RUN make devinstall

ENTRYPOINT ["rye", "run", "main.py"]
