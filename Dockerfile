FROM python:3-alpine3.10
ENV AWS_DEFAULT_REGION=ap-south-1

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8002

CMD sh -c 'python app.py'

# CMD ["sh", "bash_script.sh"]
# CMD python ./app.py

