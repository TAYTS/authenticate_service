FROM python:3.6-alpine

RUN adduser -D userbackend

WORKDIR /home/userbackend

# Install all the required libraries and dependencies
RUN apk update
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    libc-dev \
    linux-headers \
    mariadb-dev \
    python3-dev \
    postgresql-dev \
    bash \
    nginx \
    supervisor &&  \
    rm -rf /etc/nginx/conf.d

# Create python virtual environment
RUN python -m venv venv

# Copy current directory files to the container
COPY app app
COPY log log
COPY models models
COPY migrations migrations

# Install the all library inside the requirement file
RUN venv/bin/pip install -r app/requirements.txt

# Copy all the script and config files
COPY boot.sh supervisord.conf userbackend.ini wsgi.py ./

# Update supervisord config
COPY supervisord.conf /etc/supervisord.conf

# Configure nginx
COPY nginx.conf /etc/nginx/
COPY userbackend_nginx.conf /etc/nginx/conf.d/

# Change the file and directories ownership
RUN chown -R userbackend:nginx ./

# Make the boot script executable
RUN chmod +x boot.sh

# Expose port 5000
EXPOSE 5000

# Set the script to run when start up the container
ENTRYPOINT [ "./boot.sh" ]
