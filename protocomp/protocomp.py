import os

typemap = {
    "int64": ["int64_t", "int64"],
    "string": ["char*", "string"],
    "bool": ["bool", "bool"],
    "byte": ["unsigned char", "byte"],
    "bytes": ["unsigned char*", "[]byte"],
    "uint32": ["uint32_t", "uint32"],
}

cgotypeconv = {
    "int64_t" : "()"
}

class Message():
    def __init__(self, name):
        self.name = name
        self.components = []

    def add_component(self, component):
        self.components.append(component)

    def writetype(self):
        s = "struct " + self.name + "{\n"
        for component in self.components:
            s += component.writetype()
        s += "};\n\n"
        return s

    def writeCtranslator_c(self):
        s = self.name + " make_" + self.name + "("
        for component in self.components:
            s += component.c_messagetype + " " + component.name + ", "
            if component.isrepeated:
                s += "int " + component.name + "_size, "

        if self.components:
            s = s[:-2] + "){\n"
        else:
            s += "){\n"
        
        s += "  " + self.name + " _a_;\n"
        for component in self.components:
            s += "  _a_." + component.name + " = " + component.name + ";\n"
            if component.isrepeated:
                "   _a_." + component.name + "_size = " + component.name + "_size;\n"
        
        s += "  return _a_;\n};\n\n"
        return s

    def writeGOtype(self):
        s = "type " + self.name + " struct" + " {\n"
        for component in self.components:
            s += component.writeGOtype()
        s += "}\n\n"
        return s
    
    def writeCGOtranslator(self):
        s = "func (_a_ *" + self.name + ") toC() C." + self.name + " {\n"
        s += "  return C.make_" + self.name + "("
        for component in self.components:
            if component.messagetype in typemap:
                s += "(" 
                if component.isrepeated:
                    s += "*"
                msgtype = typemap[component.messagetype][0]
                if msgtype[-1] == "*":
                    msgtype = msgtype[:-1]
                    s += "*"

                s += "C."+ msgtype + ")(_a_." +  component.name + "), "
            else:
                if component.isrepeated:
                    #problem
                    pass
                else:
                    s += "_a_." + component.name + ".toC(), "
        
        if self.components:
            s = s[:-2] + ")\n"
        else:
            s += ")\n"

        s += "}\n\n"

        return s



class Component():
    def __init__(self, name, messagetype, isrepeated):
        self.name = name
        self.isrepeated = isrepeated
        self.messagetype = messagetype

        if messagetype in typemap:
            self.c_messagetype, self.go_messagetype = typemap[messagetype]
        else:
            self.c_messagetype = messagetype
            self.go_messagetype = messagetype

        if isrepeated:
            self.c_messagetype = self.c_messagetype + "*"
            self.go_messagetype = "[]" + self.go_messagetype

    def writetype(self):

        if self.isrepeated:
            s = "   " + self.c_messagetype + " " + self.name + ";\n" 
            s += "   int " + self.name + "_size;"
        
        else:
            s = "   " + self.c_messagetype + " " + self.name + ";"

        s += "\n"
        return s
    
    def writeGOtype(self):
        return "   " + self.name + " " + self.go_messagetype + "\n" 
    
class OneOf():
    def __init__(self, name, supername):
        self.name = name
        self.messagetype = supername + "_" + name
        self.c_messagetype = supername + "_" + name
        self.go_messagetype = supername + "_" + name
        self.components = []
        self.isrepeated = False

    def add_component(self, component):
        self.components.append(component)

    def writetype(self):
        return "   " + self.c_messagetype + " " + self.name + ";\n"
    
    def write_oneoftype(self):

        s = "union " + self.c_messagetype + " {\n"
        for component in self.components:
            s += component.writetype()
        s += "}; \n\n"
        return s
    
    def writeCtranslator_c(self):
        for component in self.components:
            s = self.c_messagetype + " make_" + self.c_messagetype + "_" + component.name + "("
            s += component.c_messagetype + " " + component.name
            s += "){\n"
            s += "  " + self.c_messagetype + " _a_;\n"
            s += "  _a_." + component.name + " = " + component.name + ";\n"
            s += "  return _a_;\n};\n\n"
        
        return s

    def writeGOtype(self):
        return "   " + self.name + " " + self.go_messagetype + "\n"

    def write_GOoneoftype(self):

        s = "type " + self.go_messagetype + " interface {\n"
        s += "  _is_" + self.go_messagetype + "()\n"
        s += "}\n\n"
        return s



class Parser():
    def __init__(self):
        self.messages = []
        self.oneofs = []
        self.tokens = []

    def parse_proto(self, fname):

        if self.tokens:
            raise RuntimeError("already parsed a file")

        with open(fname, "r") as f:
            lines = f.readlines()
            for line in lines:
                self.tokens += line.split()

            i = 0
            while i < len(self.tokens):
                if self.tokens[i] == "message":
                    i = self.parse_message(i+1)
                else:
                    i += 1

    def parse_message(self, i):
        name = self.tokens[i]
        opened_brackets = False
        if name[-1] == "{":
            name = name[:-1]
            open_brackets = True

        message = Message(name)

        i += 1
        while True:
            match self.tokens[i]:
                case "{":
                    if opened_brackets:
                        raise ValueError("braces don't seem right in the proto")
                    else: 
                        opened_brackets = True
                        i = i + 1

                case "oneof":
                    i, oneof = self.parse_oneof(i+1, name)
                    message.add_component(oneof)
                case ";":
                    i = i+1
                case "}":
                    break
                case _:
                    i, component = self.parse_line(i)
                    message.add_component(component)

        self.messages.append(message)
        return i + 1
    
    def parse_oneof(self, i, supername):
        name = self.tokens[i]
        opened_brackets = False
        if name[-1] == "{":
            name = name[:-1]
            open_brackets = True

        oneof = OneOf(name, supername)

        i += 1
        while True:
            match self.tokens[i]:
                case "{":
                    if opened_brackets:
                        raise ValueError("braces don't seem right in the proto")
                    else: 
                        opened_brackets = True
                        i = i + 1
                case ";":
                    i = i+1
                case "}":
                    break
                case _:
                    i, component = self.parse_line(i)
                    oneof.add_component(component)
        
        self.oneofs.append(oneof)

        return i+1, oneof
        
                

    def parse_line(self, i):
        if self.tokens[i] == "repeated":
            component = Component(self.tokens[i+2], self.tokens[i+1], True)
            i = i + 3
        else:
            component = Component(self.tokens[i+1], self.tokens[i], False)
            i = i + 2
            
        while self.tokens[i][-1] != ";":
            i += 1
        
        return i + 1, component
    
    def make_c_types(self, fname):

        s = "#include <stdint.h>\n"
        s += "#include <stdbool.h>\n\n"
        for message in self.messages:
            s += message.writetype()

        s += "\n"
        for oneofs in self.oneofs:
            s += oneofs.write_oneoftype()

        
        with open(fname, "w") as f:
            f.write(s)

    def make_GO_types(self, fname):

        s  = "package inter\n\n"

        for message in self.messages:
            s += message.writeGOtype()

        s += "\n"
        for oneofs in self.oneofs:
            s += oneofs.write_GOoneoftype()

        
        with open(fname, "w") as f:
            f.write(s)

    def makeCtranslator_c(self, fname, hfile):

        s = "#include " + '"' + hfile + '"\n\n'
        for message in self.messages:
            s += message.writeCtranslator_c()
        
        for oneofs in self.oneofs:
            s += oneofs.writeCtranslator_c()

        with open(fname, "w") as f:
            f.write(s)

    def makeCGOtranslator(self, fname):

        s = "package inter\n\n"
        s += "import C\n\n"
        for message in self.messages:
            s += message.writeCGOtranslator()
        
        with open(fname, "w") as f:
            f.write(s)




def make_files():

    fbase = "../protocol"
    proto = os.path.join(fbase, "mumax.proto")
    typefile = os.path.join(fbase, "mumax_msgtypes.h")
    makerfile = os.path.join(fbase, "mumax_msgmakers.h")
    gofile = os.path.join(fbase, "mumax_gotypes.go")
    gotransfile = os.path.join(fbase, "mumax_cgotrans.go")

    parser = Parser()
    print(len(parser.messages))
    parser.parse_proto(proto)
    parser.make_c_types(typefile)
    parser.makeCtranslator_c(makerfile, typefile)
    parser.make_GO_types(gofile)
    parser.makeCGOtranslator(gotransfile)

make_files()