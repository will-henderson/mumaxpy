all:
	protoc --go_out=. --go-grpc_out=. mumax.proto
	python3.11 -m grpc_tools.protoc -I. --python_out=../mumaxpy --pyi_out=../mumaxpy --grpc_python_out=../mumaxpy mumax.proto
	sed -i 's/import mumax_pb2 as mumax__pb2/from . import mumax_pb2 as mumax__pb2/g' ../mumaxpy/mumax_pb2_grpc.py

