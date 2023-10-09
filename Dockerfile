FROM geopraevent/python-poetry:1.6.1-python3.10-bullseye

COPY ./pyproject.toml /pyproject.toml

RUN pip install poetry
RUN poetry install

COPY ./main.py /main.py
COPY ./core /core

EXPOSE 80
EXPOSE 443

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]