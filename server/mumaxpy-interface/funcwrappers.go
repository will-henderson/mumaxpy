package main

import (
	"C"
	"unsafe"

	pb "github.com/will-henderson/mumaxpy/protocol"
	mmif "github.com/will-henderson/mumaxpy/server/interfacing"
	"google.golang.org/protobuf/proto"
)

//export Eval
func Eval(in *C.uchar, length C.int) (out []byte) {
	in_bytes := (*[1 << 30]byte)(unsafe.Pointer(in))[:length:length]
	cmd := &pb.STRING{}
	proto.Unmarshal(in_bytes, cmd)
	res, _ := mmif.Eval(cmd)
	out, _ = proto.Marshal(res)
	return out
}

func GetIdentifiers() (out [][]byte) {
	ch := make(chan (*pb.Identifier))
	go mmif.GetIdentifiers(ch)

	for {
		idf := <-ch
		idf_msg, _ := proto.Marshal(idf)
		out = append(out, idf_msg)
	}

}

func main() {}
