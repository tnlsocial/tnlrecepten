FROM python:3.9.8-slim
EXPOSE 8000
COPY . /home
WORKDIR /home
RUN pip3 install -r requirements.txt
RUN chmod +x run.sh
ENTRYPOINT ["sh","run.sh"]