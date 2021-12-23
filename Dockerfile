FROM python:3.9.9-slim-buster

WORKDIR /app

ENV VIRTUAL_ENV=/app/machinery-venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements_dev.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN pip install -e . 

ENTRYPOINT [ "sh" ]
CMD [ "/app/machinery-entrypoint.sh" ]