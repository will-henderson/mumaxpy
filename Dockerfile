FROM nvidia/cuda:11.7.1-runtime-ubuntu20.04
LABEL Author="Aithericon <contact@aithericon.com>"
LABEL Title="numpire worker"

ENV PATH="/mumax3:/agridos:${PATH}:/usr/local/go/bin"
ENV PYGRIDOS="/agridos/pygridos"
ENV PYMICROMAG="/agridos/pymicromag"
ENV TZ="Europe/Berlin"
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ="Europe/Berlin"

RUN apt-get update
RUN apt-get -y install tzdata wget
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt install -y python3.11-dev

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3-distutils \
        python3-apt \
#        ffmpeg \
        git
#RUN python3 -m pip install --upgrade pip
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.11 get-pip.py
#RUN pip3 install kaleido
#RUN pip3 install netCDF4
#RUN pip3 install scipy
#RUN pip3 install "xarray[io]"
#RUN pip3 install xrft
#RUN pip3 install scikit-image
#RUN pip3 install Jinja2

RUN mkdir /installing_stuff/

RUN mkdir /Data
RUN mkdir /Data/log
RUN mkdir /Data1
RUN mkdir /Data1/log
ENV PYTHONPATH=/usr/local/lib/python3.11/dist-packages/

ENV AGRIDOS_DATA=/Data1/

# Install go
RUN wget https://go.dev/dl/go1.21.6.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go1.21.6.linux-amd64.tar.gz

WORKDIR "/installing_stuff"
RUN git clone https://github.com/will-henderson/mumaxformumaxpy.git 3	
RUN git clone https://github.com/will-henderson/mumaxpy.git

RUN alias python='python3.11'
RUN alias python3='python3.11'

RUN python3.11 -m pip install ./mumaxpy

WORKDIR "./mumaxpy/mumaxpy-server/"
RUN go install


