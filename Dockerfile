FROM python:3
ADD .  /
RUN pip install requests
RUN pip install pyHS100
CMD [ "python", "./tplink.py" ]
