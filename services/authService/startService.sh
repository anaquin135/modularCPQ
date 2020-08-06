docker build -t authservice:latest .
docker run -d -p 601:5000 authservice
