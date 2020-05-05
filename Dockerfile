FROM python:alpine

WORKDIR /srv/www

RUN apk update \
&& apk install --no-cache git build-base \
&& git clone https://github.com/Nerevarishe/vista-portal-backend.git \
&& pip install -r --no-cache-dir ./vista-portal-backend/requirements.txt \
&& apk del git build-base

WORKDIR /srv/www/vista-portal-backend

EXPOSE 5000

VOLUME /srv/www/vista_portal_api/static/uploads

CMD gunicorn -w 4 -b 0.0.0.0:5000 vista_portal_api:app
