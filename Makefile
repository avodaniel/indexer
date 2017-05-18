.PHONY: all protobuf_backend protobuf_frontend
all: protobuf_backend protobuf_frontend

protobuf_backend: gen/py/rpc_pb2.py

gen/py/%_pb2.py: %.proto
	mkdir -p gen/py
	protoc --python_out=gen/py $<


protobuf_frontend: gen/js/rpc.js

gen/js/%.js: gen/node_js/%_pb.js
	mkdir -p gen/js
	browserify $< -o $@

gen/node_js/%_pb.js: %.proto
	mkdir -p gen/node_js
	protoc --js_out=import_style=commonjs,binary:gen/node_js $<

.PHONY: clean
clean:
	rm -vf gen
