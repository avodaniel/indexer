.PHONY: all protobuf
all: protobuf

protobuf: gen/rpc_pb2.py

gen/%_pb2.py: %.proto
	protoc --python_out=gen $<

clean:
	rm -vf gen/*_pb2.py
