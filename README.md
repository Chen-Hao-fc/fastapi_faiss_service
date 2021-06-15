# fastapi_faiss_service

## Install
```bash
conda install mkl
conda install mkl-service
conda install faiss-cpu -c pytorch
```
## prepare
- you need save your vector file in **/src/resources/init_vec.tsv** 
- init_vec.tsv file format split by ' ' 
```python
content = line.strip().split(' ')
label = content[0]
vector = [float(v) for v in content[1:]]
```

## Execute

### bash

```bash
cd fastapi_faiss_service/src
uvicorn service:app --host 0.0.0.0 --port 5000 --reload
```

### docker
```bash
cd fastapi_faiss_service && docker build -t fastapi_faiss_service:latest .
docker run -it --rm -p 6006:5000 -d fastapi_faiss_service:latest
```

## Http Request
```http request
http://localhost:6006/index/labels?k=5&labels=在,了
```

