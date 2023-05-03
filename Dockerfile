FROM python:3.7
RUN pip3 install fastapi uvicorn
RUN pip install -r requirements.txt
COPY ./app /app
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "15400" ]