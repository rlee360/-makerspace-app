FROM ubuntu:focal

ENV FLASK_ENV=development

SHELL ["/bin/bash", "-c"]

WORKDIR /app

RUN apt update && \
    apt install -y git python3 python3-venv python3-pip

RUN ls /
RUN git clone -b application https://github.com/rlee360/makerspace-app.git /app 
RUN ls /app
RUN cd backend && pip install -r requirements.txt
RUN ls /app/backend/src

# COPY ./entrypoint.sh /

# ENTRYPOINT ['/entrypoint.sh']
CMD ["bash"]

# ENTRYPOINT [ 'python3' ]
# CMD [ '/app/backend/src/app.py' ]