docker build -t prodservice:latest .
docker run -d -p 603:5000 prodservice
