docker build -t app-exam-local:1.0.0 .
docker run -d -p 5004:5001 app-exam-local:1.0.0