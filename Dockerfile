FROM python:alpine
WORKDIR /srv/www
RUN apk update \
&& apk add --no-cache git build-base \
&& git clone https://github.com/Nerevarishe/vista-portal-backend.git \
&& pip install -r ./vista-portal-backend/requirements.txt --no-cache-dir \
&& apk del git build-base
WORKDIR /srv/www/vista-portal-backend
EXPOSE 5000
VOLUME /srv/www/vista-portal-backend/static/uploads
CMD gunicorn -w 4 -b 0.0.0.0:5000 vista_portal_api:app
