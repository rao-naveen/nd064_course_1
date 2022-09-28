FROM python:3.8
LABEL maintainer="Naveen Rao"

COPY project/techtrends /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 3111/tcp

RUN ["python", "init_db.py"]
# command to run on container start
CMD [ "python", "-u", "app.py" ]
