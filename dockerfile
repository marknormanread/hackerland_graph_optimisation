FROM python:3.9-slim-buster

RUN apt update
RUN apt -y upgrade && \
    apt-get install -y git

COPY . /home
WORKDIR /home

RUN pip install -r requirements.txt 
# RUN pip install \
#     igraph \
#     numpy \
#     scipy \
#     matplotlib \
#     mypy \
#     networkx \
#     yapf


RUN pip install -e .


# Install the UNSGA3 package I wrote many years ago... Hope it still works! 
RUN mkdir -p /unsga3 && \
    cd /unsga3 && \
    git clone https://github.com/marknormanread/unsga3.git && \
    cd unsga3 && \
    python setup.py install

RUN cd /home


# Set the default command for the container.
CMD ["/bin/bash"]