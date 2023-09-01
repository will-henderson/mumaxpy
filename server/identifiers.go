package main

import (
	"reflect"
	"strings"

	en "github.com/mumax/3/engine"
	"github.com/mumax/3/script"
	pb "github.com/will-henderson/mumaxpy/protocol"
)

func (e *mumax) GetIdentifiers(in *pb.NULL, stream pb.Mumax_GetIdentifiersServer) error {

	identifiers := en.World.Identifiers
	docs := en.World.Doc

	//documentation := NewDocumentation() now storing this as a global.

	for key, doc := range docs {

		element := identifiers[strings.ToLower(key)]

		var identifier *pb.Identifier
		if element.Type().Kind() == reflect.Func {
			names, types, outtypes, docComment := documentation.DocForFunc(reflect.ValueOf(element.Eval()), false)

			if doc == "" {
				doc = docComment
			}

			fid := &pb.Identifier_F{F: &pb.Function{Argtypes: types, Argnames: names, Outtypes: outtypes}}
			identifier = &pb.Identifier{Name: key, Doc: doc, Props: fid}

		} else {
			AddType(element.Type())
			vType := element.Type().String()

			if _, ok := element.(script.LValue); ok {

				var inputType string
				if lvalin, ok := element.(interface{ InputType() reflect.Type }); ok {
					inputType = lvalin.InputType().String()
				} else {
					inputType = vType
				}

				lid := &pb.Identifier_L{L: &pb.LValue{Type: vType, Inputtype: inputType}}
				identifier = &pb.Identifier{Name: key, Doc: doc, Props: lid}

			} else {

				rid := &pb.Identifier_R{R: &pb.ROnly{Type: vType}}
				identifier = &pb.Identifier{Name: key, Doc: doc, Props: rid}

			}
		}

		err := stream.Send(identifier)
		if err != nil {
			return err
		}
	}
	return nil
}

func (e *mumax) GetTypeInfo(in *pb.STRING, stream pb.Mumax_GetTypeInfoServer) error {

	t := typeMap[in.S]
	t = baseElem(t)

	for i := 0; i < t.NumMethod(); i++ {
		err := sendMethodIdentifier(t.Method(i), stream)
		if err != nil {
			return err
		}
	}

	tptr := reflect.PointerTo(t)
	for i := 0; i < tptr.NumMethod(); i++ {
		err := sendMethodIdentifier(tptr.Method(i), stream)
		if err != nil {
			return err
		}
	}

	if t.Kind() == reflect.Struct {
		for i := 0; i < t.NumField(); i++ {
			field := t.Field(i)
			if field.IsExported() {
				err := sendFieldIdentifier(field, stream)
				if err != nil {
					return err
				}
			}
		}
	}

	return nil
}

func sendMethodIdentifier(method reflect.Method, stream pb.Mumax_GetTypeInfoServer) error {
	names, types, outtypes, docComment := documentation.DocForFunc(method.Func, true)
	identifier := &pb.Identifier{
		Name: method.Name,
		Doc:  docComment,
		Props: &pb.Identifier_F{
			F: &pb.Function{
				Argtypes: types,
				Argnames: names,
				Outtypes: outtypes,
			},
		},
	}
	return stream.Send(identifier)
}

func sendFieldIdentifier(field reflect.StructField, stream pb.Mumax_GetTypeInfoServer) error {
	identifier := &pb.Identifier{
		Name: field.Name,
		Props: &pb.Identifier_R{
			R: &pb.ROnly{
				Type: field.Type.String(),
			},
		},
	}
	return stream.Send(identifier)
}

func baseElem(t reflect.Type) reflect.Type {
	kind := t.Kind()
	if kind == reflect.Pointer || kind == reflect.Array || kind == reflect.Map || kind == reflect.Slice || kind == reflect.Chan {
		return baseElem(t.Elem())
	} else {
		return t
	}
}
