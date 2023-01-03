# pull official base image
FROM python:3.8.10-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
# prevent python from writing byte code
ENV PYTHONDONTWRITEBYTECODE 1
# prevent python from buffering stdout and sterr
ENV PYTHONBUFFERED 1

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . . 

# run 
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

