package main

import (
	"fmt"
	"go/ast"
	"go/build"
	"go/doc"
	"go/parser"
	"go/token"
	"io/fs"
	"log"
	"os"
	"reflect"
	"runtime"
	"strings"
)

type packageFunctions struct {
	functions map[string]*doc.Func
	methods   map[string]map[string]*doc.Func
}

type Documentation struct {
	packages map[string]packageFunctions
}

func NewDocumentation() Documentation {
	return Documentation{make(map[string]packageFunctions)}
}

func (d *Documentation) GetDoc(name string) *doc.Func {

	//split package and function:
	slashPos := strings.LastIndex(name, "/")
	if slashPos < 0 {
		slashPos = 0
	}

	periodPos := strings.Index(name[slashPos:], ".")
	packageName := name[:slashPos+periodPos]
	symbolName := name[slashPos+periodPos+1:]

	funcs, ok := d.packages[packageName]
	if !ok {
		funcs = generatePackageDoc(packageName)
		d.packages[packageName] = funcs
	}

	//if symbol name contains a period, it is a method.
	periodPos = strings.Index(symbolName, ".")
	if periodPos == -1 {
		return funcs.functions[symbolName]
	} else {
		className := symbolName[:periodPos]
		className = strings.ReplaceAll(className, "(", "")
		className = strings.ReplaceAll(className, ")", "")
		className = strings.ReplaceAll(className, "*", "")
		methodName := symbolName[periodPos+1:]
		methodName, _ = strings.CutSuffix(methodName, "-fm")
		return funcs.methods[className][methodName]
	}

}

func generatePackageDoc(packageName string) (pfs packageFunctions) {

	wd, _ := os.Getwd()
	pkg, _ := build.Import(packageName, wd, build.ImportComment)
	// include tells parser.ParseDir which files to include.
	// That means the file must be in the build package's GoFiles or CgoFiles
	// list only (no tag-ignored files, tests, swig or other non-Go files).
	include := func(info fs.FileInfo) bool {
		for _, name := range pkg.GoFiles {
			if name == info.Name() {
				return true
			}
		}
		for _, name := range pkg.CgoFiles {
			if name == info.Name() {
				return true
			}
		}
		return false
	}
	fset := token.NewFileSet()
	pkgs, err := parser.ParseDir(fset, pkg.Dir, include, parser.ParseComments)
	if err != nil {
		log.Fatal(err)
	}

	astPkg := pkgs[pkg.Name]

	mode := doc.AllDecls

	docPkg := doc.New(astPkg, pkg.ImportPath, mode)

	functions := make(map[string]*doc.Func)
	for _, f := range docPkg.Funcs {
		functions[f.Name] = f
	}

	methods := make(map[string]map[string]*doc.Func)
	//interfaces := make(map[string]bool)
	for _, t := range docPkg.Types {
		for _, f := range t.Funcs {
			functions[f.Name] = f
		}
		methodsT := make(map[string]*doc.Func)
		for _, f := range t.Methods {
			methodsT[f.Name] = f
		}
		methods[t.Name] = methodsT

		//interfaces[t.Name] = isInterface(t)
		//if interfaces[t.Name] {
		//	fmt.Println(t.Name)
		//	getInterfaceMethods(t)
		//}
	}

	//we then need to go through and add embedded interface types
	/*
		for _, t := range docPkg.Types {
			embedded := getEmbeddedTypes(t)
			for _, e := range embedded {
				if interfaces[e] {
					//fmt.Println(e, t.Name, methods[e])
					for k, v := range methods[e] {
						methods[t.Name][k] = v
					}
					//fmt.Println(methods[t.Name])
				}
			}

		}
	*/

	return packageFunctions{functions, methods}
}

func isInterface(t *doc.Type) bool {

	typeSpec := getTypeSpec(t)
	_, ok := typeSpec.Type.(*ast.InterfaceType)
	return ok
}

func getInterfaceMethods(t *doc.Type) []string {

	typeSpec := getTypeSpec(t)
	inter, _ := typeSpec.Type.(*ast.InterfaceType)

	for _, method := range inter.Methods.List {
		fmt.Println(method)
		function := method.Type.(*ast.FuncType)
		fmt.Println(function)
	}

	return nil
}

func getEmbeddedTypes(t *doc.Type) []string {

	names := make([]string, 0)

	typeSpec := getTypeSpec(t)

	if typeSpec == nil {
		return nil
	}

	typ, ok := typeSpec.Type.(*ast.StructType)
	if !ok {
		return nil
	}

	fields := typ.Fields.List
	for _, field := range fields {
		if len(field.Names) == 0 { //could be an embedded type.
			ty := field.Type
			switch ident := ty.(type) {
			case *ast.Ident:
				names = append(names, ident.Name)
			case *ast.SelectorExpr:
				//just ignore these for now because we don't have this case in mumax.
				//names = append(names, ident.Sel.Name)
			}
		}
	}

	return names
}

func getTypeSpec(t *doc.Type) *ast.TypeSpec {

	name := t.Name
	decl := t.Decl

	var typeSpec *ast.TypeSpec
	for _, spec := range decl.Specs {
		ts := spec.(*ast.TypeSpec) // Must succeed.
		if name == ts.Name.Name {
			typeSpec = ts
		}
	}
	return typeSpec
}

func (d *Documentation) DocForFunc(value reflect.Value, method bool) (names, types, outtypes []string, docComment string) {

	first := 0 //don't include receiver in types if method.
	if method {
		first = 1
	}

	valType := value.Type()
	for i := first; i < valType.NumIn(); i++ {
		types = append(types, valType.In(i).String())
		AddType(valType.In(i))
	}

	for i := 0; i < valType.NumOut(); i++ {
		outtypes = append(outtypes, valType.Out(i).String())
		AddType(valType.Out(i))
	}

	funcdetail := runtime.FuncForPC(value.Pointer())
	funcdoc := d.GetDoc(funcdetail.Name())
	if funcdoc == nil { //probably a type from an embedded interface so just make up some stuff.
		docComment = ""
		name := 'a'
		for i := 0; i < len(types); i++ {
			names = append(names, string(name))
			name++
		}
	} else {
		docComment = funcdoc.Doc

		params := funcdoc.Decl.Type.Params
		if params != nil {
			for _, p := range params.List {
				for _, name := range p.Names {
					names = append(names, name.Name)
				}
			}
		}
	}

	return names, types, outtypes, docComment

}
