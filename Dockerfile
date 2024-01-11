FROM python:3.8
RUN apt-get update && apt-get install -y redis-tools
WORKDIR /home/test_user/Downloads/kiran/Dramatiq
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn
COPY . .
CMD ["/usr/local/bin/uvicorn", "uvicorn", "basic:app", "--host", "0.0.0.0", "--port", "8000"]

