FROM python:3-slim
RUN pip install -U cffi PyGithub
ADD . /app
WORKDIR /app
RUN chmod +x "/app/main.py"

CMD ["python3", "/app/main.py"]