FROM python:3.10-slim-bookworm as prod

RUN apt update && \
    apt install -y make curl && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

ARG USERNAME=ryeuser
RUN useradd -ms /bin/bash ${USERNAME} --create-home
USER ${USERNAME}
WORKDIR /home/${USERNAME}/highscore-micro-two
COPY . .
RUN pip install -r requirments.lock

ENTRYPOINT ["rye", "run", "main.py"]
