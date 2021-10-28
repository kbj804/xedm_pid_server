# Docker Build
docker build -t aiocr:0.1 .

# Docker Run
docker run -d --name aiocr -v /deploy/aiocr/aiocr/docker/input:/aiocr/input -v /deploy/aiocr/aiocr/docker/output:/aiocr/output aiocr:0.1

# Execute Python Script 
docker exec aiocr python aiocr.py
