module github.com/will-henderson/mumaxpy

go 1.21.6

require (
	github.com/mumax/3 v3.9.3+incompatible
	google.golang.org/grpc v1.61.0
	google.golang.org/protobuf v1.31.0
)

require (
	github.com/golang/protobuf v1.5.3 // indirect
	golang.org/x/net v0.18.0 // indirect
	golang.org/x/sys v0.14.0 // indirect
	golang.org/x/text v0.14.0 // indirect
	google.golang.org/genproto/googleapis/rpc v0.0.0-20231106174013-bbf56f31fb17 // indirect
)

replace github.com/mumax/3 => ../3
