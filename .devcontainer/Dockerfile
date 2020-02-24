
ARG UBUNTU_VERSION=18.04

FROM nvidia/cuda:10.1-cudnn7-devel-ubuntu${UBUNTU_VERSION} as base
ENV NVIDIA_DRIVER_CAPABILITIES ${NVIDIA_DRIVER_CAPABILITIES},display

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends \
        mesa-utils \
        build-essential \
        sudo \
        cmake \
        libgtk2.0-dev \
        libgtk-3-dev \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        libfreetype6-dev \
        libhdf5-serial-dev \
        unzip \
        zip \
        libzmq3-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libeigen3-dev \
        libdc1394-22-dev \
        pkg-config \
        software-properties-common \
        unzip \
        zip \
        wget \
        git \
        vim \
        curl \
        libssl-dev \
        lldb \
        procps \
        lsb-release \
        x11-xserver-utils \
        libmagick++-dev \
        python3-dev \ 
        python3-setuptools

# I'm not sure about --allow-change-held-packages
RUN apt install -y --allow-change-held-packages libnccl2 \
        libnccl-dev \ 
        libyaml-dev


# OpenCV 4 
# Remove old OpenCV
RUN apt remove --purge -y libopencv-dev

# Compile OpenCV 4.1.1
RUN git clone https://github.com/opencv/opencv.git
WORKDIR /opencv
#RUN git checkout 4.1.1
RUN mkdir build
WORKDIR /opencv/build
RUN cmake \
    -D CMAKE_BUILD_TYPE=Release \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D BUILD_EXAMPLES=OFF \
    -D BUILD_PERF_TESTS=OFF \
    -D BUILD_TESTS=OFF \
    -D BUILD_DOCS=OFF \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D ENABLE_PRECOMPILED_HEADERS=OFF \
    ..
RUN make -j$(nproc)
RUN make install
RUN ldconfig

ARG USERNAME=sim
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Non-root user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && mkdir -p /home/$USERNAME/.vscode-server /home/$USERNAME/.vscode-server-insiders \
    && chown ${USER_UID}:${USER_GID} /home/$USERNAME/.vscode-server* \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && usermod -a -G audio,video $USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    # Clean up
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

#add environment variable and change python alias
COPY  bashrc /etc/bash.bashrc
RUN chmod a+rwx /etc/bash.bashrc
RUN update-alternatives --remove python /usr/bin/python2
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10




USER $USERNAME
ENV HOME /home/$USERNAME
WORKDIR $HOME
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN sudo python3 get-pip.py

#        python3-numpy \
#        python3-pip \
#        python3-tk \

#Pytorch
RUN sudo pip install torch torchvision  
RUN sudo pip install onnx>=1.6 
RUN sudo pip install opencv-python>=3.4 
RUN sudo pip install numpy>=1.17

# Symlink for python3
RUN sudo ln -s /usr/bin/pip3 /usr/bin/pip

# Download the model
RUN sudo mkdir /models 
WORKDIR /models
RUN sudo wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1niBUbUecPhKt3GyeDNukobL4OQ3jqssH' -O human-pose-estimation-3d.pth
