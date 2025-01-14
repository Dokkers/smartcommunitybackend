# 使用官方Python 3.8镜像作为基础镜像
FROM python:3.8

# 设置工作目录为/app
WORKDIR /app

# 将当前目录下的所有文件复制到工作目录下
COPY . /app

# RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装依赖，这里假设你的依赖在requirements.txt文件中
# RUN pip install -r requirements.txt --ignore-installed -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt --ignore-installed -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple/

# 设置环境变量，如果需要的话
# ENV NAME World

# 暴露端口，根据你的应用需要暴露的端口来设置
EXPOSE 5000

# 容器启动时执行的命令
CMD ["python", "run.py"]