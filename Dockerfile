FROM python:3.7
COPY requirements.txt /

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
ENV TZ="America/Chicago"

# Installing because if just installing from requirements.txt then error thrown
# saying gunicorn not in environment path. This fixed it
RUN pip install gunicorn

# this directory /template should be the same name of your package folder
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
