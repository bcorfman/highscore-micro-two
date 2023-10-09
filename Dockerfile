FROM geopraevent/python-poetry:1.6.1-python3.10-bullseye

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml

RUN pip install poetry
RUN poetry install

COPY ./main.py /code/main.py
COPY ./core /code/core

EXPOSE 80
EXPOSE 443

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "443"]