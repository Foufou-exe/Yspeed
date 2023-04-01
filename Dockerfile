FROM ubuntu:latest
MAINTAINER foufou-exe

# Install dependencies
RUN apt-get update -y

# Install Python
RUN apt-get install -y git curl python3-pip python3-dev build-essential

RUN cd /

# Clone the repository
RUN git clone https://github.com/Foufou-exe/Yspeed.git

WORKDIR /Yspeed

# Install the requirements
RUN pip3 install -r /Yspeed/requirements.txt

# Expose the port
EXPOSE 22


