FROM python:alpine

WORKDIR /srv/www/vista_portal_api/

COPY . .

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 5000

VOLUME /srv/www/vista_portal_api/static/uploads

CMD gunicorn -w 4 -b 0.0.0.0:5000 vista_portal_api:app
