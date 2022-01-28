FROM python:3.7
COPY requirements.txt /

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
ENV TZ="America/Chicago"

RUN pip install gunicorn

COPY . /template
WORKDIR /template

RUN export PYTHONPATH=/app:$PYTHONPATH
RUN python setup.py install

CMD ["gunicorn", \
     "--threads", "3", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--timeout", "600", \
     "--bind", "0.0.0.0:7777", \
     "--graceful-timeout", "500", \
     "template:create_app()"]
