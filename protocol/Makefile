all:
	protoc --go_out=. --go_opt=paths=source_relative --go-grpc_out=. --go-grpc_opt=paths=source_relative mumax.proto

	python -m grpc_tools.protoc -I. --python_out=../mumaxpy --pyi_out=../mumaxpy --grpc_python_out=../mumaxpy mumax.proto