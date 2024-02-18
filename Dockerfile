FROM python:3.10-slim-bookworm as prod

RUN apt update && \
    apt install -y make curl && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

ARG USERNAME=ryeuser
RUN useradd -ms /bin/bash ${USERNAME} --create-home
USER ${USERNAME}
WORKDIR /home/${USERNAME}/highscore-micro-two
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements-dev.lock

EXPOSE 80
EXPOSE 443
ENTRYPOINT ["python", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443"]
