# indexer

## installation

For backend make sure that make, python >= 3.6 and protoc >= 3.3.0
(protobuf compiler) are installed and runnable from command line.

If you want to build JS libraries for frontend make sure that npm >= 3.10.10,
python >= 2.7 and protoc >= 3.3.0 with JS support are installed and runnable
from command line.

Here is a quic how-to for building of protobuf from source with support of JS:

    $ wget 'https://github.com/google/protobuf/releases/download/v3.3.0/protobuf-cpp-3.3.0.tar.gz'
    $ wget 'wget https://github.com/google/protobuf/releases/download/v3.3.0/protobuf-js-3.3.0.tar.gz'
    $ tar xvf protobuf-cpp-3.3.0.tar.gz
    $ tar xvf protobuf-js-3.3.0.tar.gz
    $ cd protobuf-3.3.0
    protobuf-3.3.0 $ ./configure --prefix=/opt/protobuf-3.3.0 && make -j8
    protobuf-3.3.0 # make install
    export PATH=/opt/protobuf-3.3.0/bin:$PATH

Instalation of npm is described at: [NPM Installation](wget https://github.com/google/protobuf/releases/download/v3.3.0/protobuf-js-3.3.0.tar.gz).

### Debian/Ubuntu

    # apt-get install libczmq-dev
    
### Fedora/CentOS/RH

    # yum install zeromq-devel
    
### On all OSes

For backend, install necessary python packages:

    # pip3 install pyzmq --install-option="--zmq=/usr/lib"
    # pip3 install python-bitcoinlib
    # pip3 install leveldb
    # pip3 install websockets
    # pip3 install protobuf

For frontend, install following npm (NodeJS) packages:

    # npm install uniq
    # npm install browserify
    # npm install google-protobuf
