FROM python:3

ADD liveness.py /

#RUN pip install pystrich

CMD [ "python", "./liveness.py" ]