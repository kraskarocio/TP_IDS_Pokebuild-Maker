FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /app && cd /app
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY ./app /app
EXPOSE 5000
CMD ["python", "app.py"]