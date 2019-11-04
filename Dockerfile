FROM python:3

RUN pip3 install redis

COPY server.py /

EXPOSE 65432

ENTRYPOINT ["python3", "server.py"]
