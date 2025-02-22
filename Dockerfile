FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
 && apt-get install --yes --no-install-recommends \
        apt-transport-https \
        curl \
        gnupg \
        unixodbc-dev \
 && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update \
 && ACCEPT_EULA=Y apt-get install --yes --no-install-recommends msodbcsql17 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* \
 && rm -rf /tmp/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV SQL_SERVER_HOST=$(SQL_SERVER_HOST)
ENV SQL_SERVER_DATABASE=$(SQL_SERVER_DATABASE)
ENV SQL_SERVER_USERNAME=$(SQL_SERVER_USERNAME)
ENV SQL_SERVER_PASSWORD=$(SQL_SERVER_PASSWORD)

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5005

CMD [ "flask", "run", "--host", "0.0.0.0", "--port", "5005"]