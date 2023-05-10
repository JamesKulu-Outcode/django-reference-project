FROM python:3.9.6-slim  

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 0

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y libpq-dev gcc libpangocairo-1.0-0 fonts-deva netcat gettext

# COPY requirements.txt /code/
# install dependencies
RUN pip install --upgrade pip
COPY requirements .
# COPY ./requirements.txt .
RUN pip install -r development.txt


# remove build dependencies
RUN apt-get autoremove -y gcc

# copy entrypoint.sh
COPY ./entrypoint.sh .

# copy project
COPY . .

# run entrypoint.sh
# ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]

