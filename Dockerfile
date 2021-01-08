FROM arm32v7/python:3
COPY alarm_detect.py requirements.txt ./
RUN pip3 install -r requirements.txt

CMD ["python3","./alarm_detect.py","--privileged"]




