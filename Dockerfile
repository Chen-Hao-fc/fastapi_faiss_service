FROM nvcr.io/nvidia/pytorch:21.03-py3
RUN rm -rf /workspace/*
COPY src /workspace
RUN conda install mkl
RUN conda install mkl-service
RUN conda install faiss-cpu -c pytorch
RUN pip install uvicorn fastapi -i https://mirrors.aliyun.com/pypi/simple/
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/lcoaltime
RUN echo 'Asia/Shanghai' >/etc/timezone
ENV PORT 5000
WORKDIR /workspace
CMD uvicorn service:app --host 0.0.0.0 --port 5000 --reload