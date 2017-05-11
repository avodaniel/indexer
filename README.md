# indexer

## installation

### Debian/Ubuntu

    # apt-get install libczmq-dev
    
### Fedora/CentOS/RH

    # yum install zeromq-devel
    
### On all OSes

Make sure that protobuf 3.3.0 compiler is installed and is runable from
command-line (PATH variable is set accordingly).

Eg. you can build protobuf from source:

    $ wget 'https://github.com/google/protobuf/releases/download/v3.3.0/protobuf-cpp-3.3.0.tar.gz'
    $ tar xvf protobuf-cpp-3.3.0.tar.gz
    $ cd protobuf-3.3.0
    protobuf-3.3.0 $ ./configure --prefix=/opt/protobuf-3.3.0 && make -j8
    protobuf-3.3.0 # make install
    
Install necessary python packages:

    # pip3 install pyzmq --install-option="--zmq=/usr/lib"
    # pip3 install python-bitcoinlib
    # pip3 install leveldb
    # pip3 install websockets
    # pip3 install protobuf
