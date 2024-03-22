FROM python:3.8-slim

LABEL maintainer="1436381036@qq.com"

WORKDIR /app

COPY requirements.txt .

# 设置清华源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --no-cache-dir -r requirements.txt

COPY data /app/data
COPY utils /app/utils
COPY data.pickle /app/
COPY model.p /app/
COPY remain.py /app/
COPY main.py /app/

EXPOSE 8765

CMD ["python", "main.py"]