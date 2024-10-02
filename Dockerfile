# 使用官方Python运行时作为父镜像
FROM python:3.10-slim

# 设置工作目录为/app
WORKDIR /app

# 将当前目录内容复制到容器的/app中
COPY . /app

# 安装requirements.txt中指定的任何需要的包
RUN pip install --no-cache-dir -r requirements.txt

# 让端口8000可以从容器外部访问
EXPOSE 8000

# 定义环境变量
ENV NAME World

# 运行app.py当容器启动时
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]