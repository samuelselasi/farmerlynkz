FROM python:3.8.10
WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# RUN pip install pipenv
# CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "81"]