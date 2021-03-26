FROM python:3
RUN pip install mysql-connector-python
ADD main.py . 
ADD sample-data.json .
CMD [ "python", "./main.py", "sample-data.json" ]
