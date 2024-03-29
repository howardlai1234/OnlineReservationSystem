FROM python:3.8

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools

WORKDIR /opt/ors

COPY requirements.txt ./
RUN pip install -r requirements.txt

EXPOSE 8000
COPY ./ ./
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]