FROM python:3.10.12-buster
EXPOSE 8080

WORKDIR /usr/app/user_service
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/usr/app/.
RUN apt update
RUN pip install --upgrade pip
RUN pip install poetry
COPY . .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi