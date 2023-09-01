
def functionCall(name, argnames, argtypes):
    argString = []
    argInt = []
    argBool = []
    argDouble = []
    argMumax = []
    argScalarFunction = []
    argVectorFunction = []

    for argname, argtype in zip(argnames, argtypes):
        match argtype:
            case "int":
                argInt.append("int(" + argname + ")")
            case "string":
                argString.append("str(" + argname + ")" )
            case "bool":
                argBool.append(argname)
            case "float32" | "float64":
                argDouble.append(argname)
            case "data.Vector":
                argDouble.append(", ".join([argname + "[" + str(i) + "]" for i in range(3)] ))  
            case "script.ScalarFunction":
                argScalarFunction.append("_makeScalarFunction(" + argname +")")
            case "script.VectorFunction":
                argVectorFunction.append("_makeVectorFunction(" + argname +")")
   
            case _: #need to preprocess these!!
                argMumax.append("_pam(" + argname + ")") 
 
    #as this will be inside a function, we indent. 
    s =  "    fc = mumax_pb2.FunctionCall(name='" + name + "', "
    s +=      "argString=" + "[" + ", ".join(a for a in argString) + "], "
    s +=      "argBool=" + "[" + ", ".join(a for a in argBool) + "], "
    s +=      "argDouble=" + "[" + ", ".join(a for a in argDouble) + "], "
    s +=      "argInt=" + "[" + ", ".join(a for a in argInt) + "], "
    s +=      "argMumax=" + "[" + ", ".join(a for a in argMumax) + "], \n"
    s +=      "argScalarFunction=" + "[" + ", ".join(a for a in argScalarFunction) + "], \n"
    s +=      "argVectorFunction=" + "[" + ", ".join(a for a in argVectorFunction) + "])\n"

    return s

def docComment(doc, argnames, argtypes):
    doc = doc.replace("'", "\\'")

    s = "    '''\n" 
    s += "    " + doc + "\n"
    s += "    Parameters:\n"
    for argname, argtype in zip(argnames, argtypes):
        s += "        " + argname + " (" + argtype + "):\n"
    s += "    '''\n"

    return s

def returnLine(outtypes, isMM):

    out = []
    nOutString = 0
    nOutBool = 0
    nOutDouble = 0
    nOutInt = 0
    nOutMumax = 0
    nOutArray = 0
    for outtype in outtypes:

        if "[" in outtype or outtype == "data.Vector": #our crude way of detecting array outputs ehh, actually, really should do something better. 
            out.append("_processArray(reply.outArray[" + str(nOutArray) +"])")
            nOutArray += 1
        else:
            match outtype:
                case "int":
                    out.append("reply.outInt[" + str(nOutInt) + "]")
                    nOutInt += 1
                case "string":
                    out.append("reply.outString[" + str(nOutString) + "]")
                    nOutString += 1
                case "bool":
                    out.append("reply.outBool[" + str(nOutBool) + "]")
                    nOutBool += 1
                case "float32" | "float64":
                    out.append("reply.outDouble[" + str(nOutDouble) + "]")
                    nOutDouble += 1
                case "data.Vector":
                    out.append("[" + ", ".join(["reply.outDouble[" + str(nOutDouble + i) + "]" for i in range(3)]) + "]")
                    nOutDouble += 3 
                
                case _:
                    if isMM:
                        out.append("toObj(reply.outMumax[" + str(nOutMumax) + "], '" + outtype + "', self)")
                    else:
                        out.append("toObj(reply.outMumax[" + str(nOutMumax) + "], '" + outtype + "', self.master)")
                    nOutMumax += 1    

    s = "    return " + ", ".join(out) + "\n"

    return s

def functionString(name, argnames, argtypes, outtypes, doc):

    s  = "def f(self, " +  ", ".join(argnames) + "):\n" 
    s += docComment(doc, argnames, argtypes)
    s += functionCall(name.lower(), argnames, argtypes)
    s += "    reply = self.stub.Call(fc) \n"
    s += returnLine(outtypes, True)
    s += "self." + name + " = f.__get__(self)"  
    return s


def methodString(mthname, argnames, argtypes, outtypes, doc):

    s  = "def f(self, " +  ", ".join(argnames) + "):\n" 
    s += docComment(doc, argnames, argtypes)
    s += functionCall(mthname, argnames, argtypes)
    s += "    mthcall = mumax_pb2.MethodCall(mmobj=self.identifier, fc=fc)\n" 
    s += "    reply = self.master.stub.CallMethod(mthcall) \n"
    s += returnLine(outtypes, False)
    s += "classdict['" + mthname +"'] = f"

    return s

def lValueSetString(name, intype):

    setstring = "def set(self, value):\n"
    setstring += "    identifier = mumax_pb2.MumaxObject(name='" + name.lower() + "')\n"

    match intype:
        case "bool":
            setstring += "    try:\n"
            setstring += "        value = bool(value)\n"
            setstring += "    except:\n"
            setstring += "        raise TypeError('" + name + " takes a boolean input to set')\n"
            setstring += "    res = self.stub.SetBool(mumax_pb2.BoolSet(mmobj=identifier, s=value))\n"
        case "float32" | "float64":
            setstring += "    try:\n"
            setstring += "        value = float(value)\n"
            setstring += "    except:\n"
            setstring += "        raise TypeError('" + name + " takes a float input to set')\n"
            setstring += "    res = self.stub.SetDouble(mumax_pb2.DoubleSet(mmobj=identifier, s=value))\n"
        case "int":
            setstring += "    try:\n"
            setstring += "        value = int(value)\n"
            setstring += "    except:\n"
            setstring += "        raise TypeError('" + name + " takes a integer input to set')\n"
            setstring += "    res = self.stub.SetInt(mumax_pb2.IntSet(mmobj=identifier, s=value))\n"
        case "data.Vector":
            setstring += "    try:\n"
            setstring += "        value = list(value)\n"
            setstring += "        if len(value) != 3: raise TypeError()\n"
            setstring += "        value = [float(v) for v in value]\n"
            setstring += "    except:\n"
            setstring += "        raise TypeError('" + name + " takes a list-like object of floats of length 3 to set')\n"
            setstring += "    res = self.stub.SetVector(mumax_pb2.VectorSet(mmobj=identifier, x=value[0], y=value[1], z=value[2]))\n"

        case "script.ScalarFunction":
            setstring += "    self.stub.SetScalarFunction(mumax_pb2.ScalarFunctionSet(mmobj=identifier, s=_makeScalarFunction(value)))\n"

        case "script.VectorFunction":
            setstring += "    self.stub.SetVectorFunction(mumax_pb2.VectorFunctionSet(mmobj=identifier, s=_makeVectorFunction(value)))\n"

        case _: 
            setstring += "    if not hasattr(value, 'identifier'): raise TypeError('The value should be a mumax object here.')\n"
            setstring += "    self.stub.SetMumax(mumax_pb2.MumaxSet(mmobj=identifier, s=value.identifier))\n"
        #case "engine.OutputFormat":
        #
        #case "engine.FixedLayerPosition":
        #    setstring += "    if not isinstance(value, engine.FixedLayerPosition): raise TypeError('" + name + " takes input FIXEDLAYER_TOP or FIXED_LAYER bottom')\n"
        #    setstring += "    res = self.stub.SetMumax()"

    return setstring
        
def getString(name, vtype):

    getstring =  "def get(self):\n"
    getstring += "    req = mumax_pb2.MumaxObject(name='" + name.lower() + "')\n"

    match vtype:
        case "int":
            getstring += "    res = self.stub.GetInt(req).s\n"
        case "bool":
            getstring += "    res = self.stub.GetBool(req).s\n"
        case "string":
            getstring += "    res = self.stub.GetString(req).s\n"
        case "float32" | "float64":
            getstring += "    res = self.stub.GetDouble(req).s\n"
        case _:
            getstring += "    res = toObj(req, '" + vtype + "', self)\n"
    
    getstring += "    return res\n"
    return getstring


def rOnlyString(name, vtype, doc):

    s = getString(name, vtype)
    s += "Mumax." + name + " = property("
    s += "fget=get, "
    s += "doc='" + doc.replace("'", "\\'") + "')"

    return s

def lValueString(name, vtype, intype, doc):

    s = getString(name, vtype) + lValueSetString(name, intype)
    s += "Mumax." + name + " = property("
    s += "fget=get, fset=set, "
    s += "doc='" + doc.replace("'", "\\'") + "')"

    return s

def fieldString(name, ftype, doc):

    getstring =  "def get(self):\n"
    getstring += "    req = mumax_pb2.MumaxField(mmobj=self.identifier, fieldName='" + name + "')\n"

    match ftype:
        case "int":
            getstring += "    res = self.stub.GetFieldInt(req).s\n"
        case "bool":
            getstring += "    res = self.stub.GetFieldBool(req).s\n"
        case "string":
            getstring += "    res = self.stub.GetFieldString(req).s\n"
        case "float32" | "float64":
            getstring += "    res = self.stub.GetFieldDouble(req).s\n"
        case _:
            getstring += "    res = toObj(self.stub.GetFieldMumax(req), '" + ftype + "', self)\n"

    
    getstring += "    return res\n"

    s = getstring
    s += "classdict['" + name + "'] = property("
    s += "fget=get, "
    s += "doc='" + doc.replace("'", "\\'") + "')\n"

    return s
