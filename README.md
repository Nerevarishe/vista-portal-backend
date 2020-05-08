### Commands to build dev image with python libraries and image for testing:
first run:
`docker build -t nerevarishe/vista-portal-backend:dev -f ./Dockerfile-dev-first-stage . --no-cache`
then run:
`docker build -t nerevarishe/vista-portal-backend:latest -f ./Dockerfile-dev-second-stage . --no-cache`