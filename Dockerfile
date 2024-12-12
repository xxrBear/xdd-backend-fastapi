# 使用 Python 3.11 镜像作为基础镜像
FROM  docker.1ms.run/library/python:3.11-slim

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到容器中的工作目录
COPY . /app

# 安装项目依赖 (如果有 requirements.txt 文件)
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 暴露容器的 8102 端口 (根据需求修改)
EXPOSE 8102

# 默认启动命令
CMD ["sh", "-c", "python init_db.py && uvicorn main:app --host 0.0.0.0 --port 8102"]
