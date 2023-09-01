package main

import (
	"fmt"
	"reflect"
	"testing"

	en "github.com/mumax/3/engine"
)

type TypeProperties struct {
	methods []reflect.Method
	fields  []reflect.StructField
}

type RelevantTypes struct {
	typelist map[reflect.Type]TypeProperties
}

func NewRelevantTypes() RelevantTypes {
	rt := RelevantTypes{make(map[reflect.Type]TypeProperties)}
	rt.Find()
	return rt
}

func (r *RelevantTypes) Find() {
	identifiers := en.World.Identifiers
	for _, element := range identifiers {
		r.ProcessType(element.Type())
	}

}

func (r *RelevantTypes) ProcessType(t reflect.Type) {

	t = baseElem(t)
	_, ok := r.typelist[t]

	if !ok {
		if t.Kind() == reflect.Func {

			for i := 0; i < t.NumIn(); i++ {
				r.ProcessType(t.In(i))
			}
			for i := 0; i < t.NumOut(); i++ {
				r.ProcessType(t.Out(i))
			}

		} else {
			r.typelist[t] = TypeProperties{}

			var methods []reflect.Method
			for i := 0; i < t.NumMethod(); i++ {
				methods = append(methods, t.Method(i))
				r.ProcessType(t.Method(i).Type)
			}

			tptr := reflect.PointerTo(t)
			for i := 0; i < tptr.NumMethod(); i++ {
				methods = append(methods, tptr.Method(i))
				r.ProcessType(tptr.Method(i).Type)
			}

			var fields []reflect.StructField

			if t.Kind() == reflect.Struct {
				for i := 0; i < t.NumField(); i++ {
					field := t.Field(i)
					if field.IsExported() {
						fields = append(fields, t.Field(i))
						r.ProcessType(t.Field(i).Type)
					}
				}
			}
			r.typelist[t] = TypeProperties{methods, fields}
		}
	}
}

func TestBasic(p *testing.T) {

	defer en.InitAndClose()()

	magnetisation := en.World.Identifiers["m"]
	t := reflect.ValueOf(magnetisation.Eval()).Type()

	for i := 0; i < t.NumMethod(); i++ {
		fmt.Println(t.Method(i))
	}

	tptr := reflect.PointerTo(t)
	for i := 0; i < tptr.NumMethod(); i++ {
		fmt.Println(tptr.Method(i))
	}

	if t.Kind() == reflect.Struct {
		for i := 0; i < t.NumField(); i++ {
			field := t.Field(i)
			if field.IsExported() {
				fmt.Println(field)
			}
		}
	}

	generatePackageDoc("github.com/mumax/3/engine")

	sf := en.ScalarField{}
	sf.NComp()

}
