package mumaxpyinterface

import (
	pb "github.com/will-henderson/mumaxpy/protocol"
	mmif "github.com/will-henderson/mumaxpy/server/interfacing"
	"google.golang.org/protobuf/proto"
)

func Eval(in []byte) (out []byte) {
	cmd := &pb.STRING{}
	proto.Unmarshal(in, cmd)
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
