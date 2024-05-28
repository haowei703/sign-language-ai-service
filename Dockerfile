FROM python:3.8-slim

LABEL maintainer="1436381036@qq.com"

WORKDIR /app

COPY requirements.txt .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir opencv-python-headless

COPY grpc_pub /app/grpc_pub
COPY utils /app/utils
COPY data.pickle /app/
COPY model.p /app/
COPY remain.py /app/
COPY main.py /app/

EXPOSE 10123

CMD ["python", "main.py"]