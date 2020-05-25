FROM python:3.7

EXPOSE 800

WORKDIR /Aviation-Winners

RUN pip install -r ../requirements.txt
CMD python -u server.py