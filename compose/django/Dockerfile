FROM python:3.6.10-buster

RUN apt update
RUN apt-get install build-essential

# set environment variables
## Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1

## Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# specify app or project home
# ENV APP_HOME /home/django/app
ENV APP_HOME /src

# Creating Work Directory
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME
RUN mkdir static media

# Update pip
RUN pip install --upgrade pip

# Installing requirements.txt from project
COPY ./requirements.txt $APP_HOME

# RUN pip install --no-cache-dir -r $APP_HOME/requirements.txt
RUN pip install -r $APP_HOME/requirements.txt

# change folder permissions
RUN chmod -R 777 $APP_HOME

# CMD will run when this dockerfile is running
CMD ["sh", "-c", "python manage.py collectstatic --no-input; python manage.py makemigrations; python manage.py migrate; python manage.py loaddata db.json; gunicorn image_recognition_project.wsgi -b 0.0.0.0:8000 & celery -A image_recognition_project worker -l info -B"]
