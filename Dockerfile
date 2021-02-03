FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app
RUN pip install pipenv
RUN pip install -r requirements.txt 
EXPOSE 81
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "81"]