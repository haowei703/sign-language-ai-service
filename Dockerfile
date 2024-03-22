FROM python:3.8-slim

LABEL maintainer="1436381036@qq.com"

WORKDIR /app

COPY requirements.txt .

# 设置清华源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8765

CMD ["python", "main.py"]