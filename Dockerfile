FROM python:3.9
COPY . /app
WORKDIR /app

RUN pip config set global.index-url https://mirror.baidu.com/pypi/simple
RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]