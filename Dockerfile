# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.9

# Send stdout/stderr out, do not buffer.
# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED 1

# Copy application dependency manifests to the container image.
# Copying this separately prevents re-running pip install on every code change.
COPY requirements.txt ./

RUN pip3 install --upgrade setuptools
RUN apt-get install libpq-dev

# Install production dependencies.
RUN set -ex; \
    pip install -r requirements.txt;

# Copy local code to the container image.
WORKDIR /app
COPY . .

# # Service must listen to $PORT environment variable.
# # This default value facilitates local development.
# ENV PORT 8080
#
# # Run the web service on container startup. Here we use the gunicorn
# # webserver, with one worker process and 8 threads.
# # For environments with multiple CPU cores, increase the number of workers
# # to be equal to the cores available.
# # Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app

# RUN python -m nltk.downloader all
# RUN python -m nltk.downloader -d /usr/local/share/nltk_data all

ENTRYPOINT ["python", "listing_quality_score/listing_score.py"]