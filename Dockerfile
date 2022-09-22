FROM python:3.8
LABEL maintainer="Naveen Rao"

COPY . /app
WORKDIR /app
RUN pip install -r project/techtrends/requirements.txt
EXPOSE 3111/tcp

RUN ["python", "project/techtrends/init_db.py"]
# command to run on container start
CMD [ "python", "-u", "project/techtrends/app.py" ]

