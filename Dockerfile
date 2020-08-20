FROM python:3

ADD datacodetest_arunmathew.py /

RUN pip install json
RUN pip install random
RUN pip install string
RUN pip install struct
RUN pip install sys
RUN pip install csv

CMD [ "python", "./data-code-kata-master/datacodetest_arunmathew.py" ]