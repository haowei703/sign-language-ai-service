# 第一阶段：设置系统类型和安装 libgl1-mesa-glx
FROM ubuntu AS system-detector
RUN apt-get update
RUN apt-get install -y procps
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install libgl1
RUN echo "Linux" > /system-type

# 第二阶段：安装 Python 应用所需的环境
FROM python:3.8-slim

LABEL maintainer="1436381036@qq.com"

WORKDIR /app

COPY --from=system-detector /system-type /

COPY requirements.txt .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install opencv-python-headless

COPY data /app/data
COPY grpc_pub /app/grpc_pub
COPY utils /app/utils
COPY data.pickle /app/
COPY model.p /app/
COPY remain.py /app/
COPY main.py /app/

EXPOSE 10123

CMD ["python", "main.py"]