FROM python:3.9.9-buster

WORKDIR /app

ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install flask

COPY . .

ENTRYPOINT [ "sh" ]
CMD [ "/app/entrypoint.sh" ]