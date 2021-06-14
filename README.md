# fastapi_faiss_service

## Install
```bash
conda install mkl
conda install mkl-service
conda install faiss-cpu -c pytorch
```

## Execute
```bash
cd fastapi_faiss_service && docker build -t fastapi_faiss_service:latest .
docker run -it --rm -p 6006:5000 -d fastapi_faiss_service:latest
```

## https
```http request
http://localhost:6006/faiss?labels='开心'&k=5
http://localhost:6006/faiss?labels='开心'&k=5

```

