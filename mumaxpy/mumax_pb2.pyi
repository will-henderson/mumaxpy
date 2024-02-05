from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NULL(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class STRING(_message.Message):
    __slots__ = ("s",)
    S_FIELD_NUMBER: _ClassVar[int]
    s: str
    def __init__(self, s: _Optional[str] = ...) -> None: ...

class STRINGs(_message.Message):
    __slots__ = ("s",)
    S_FIELD_NUMBER: _ClassVar[int]
    s: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, s: _Optional[_Iterable[str]] = ...) -> None: ...

class BOOL(_message.Message):
    __slots__ = ("s",)
    S_FIELD_NUMBER: _ClassVar[int]
    s: bool
    def __init__(self, s: bool = ...) -> None: ...

class BOOLs(_message.Message):
    __slots__ = ("s",)
    S_FIELD_NUMBER: _ClassVar[int]
    s: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, s: _Optional[_Iterable[bool]] = ...) -> None: ...

class INT(_message.Message):
    __slots__ = ("s",)
    S_FIELD_NUMBER: _ClassVar[int]
    s: int
    def __init__(self, s: _Optional[int] = ...) -> None: ...

class INTs(_message.Message):
    __slots__ = ("s",)
    S_FIELD_NUMBER: _ClassVar[int]
    s: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, s: _Optional[_Iterable[int]] = ...) -> None: ...

class DOUBLE(_message.Message):
    __slots__ = ("s",)
    S_FIELD_NUMBER: _ClassVar[int]
    s: float
    def __init__(self, s: _Optional[float] = ...) -> None: ...

class DOUBLEs(_message.Message):
    __slots__ = ("s",)
    S_FIELD_NUMBER: _ClassVar[int]
    s: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, s: _Optional[_Iterable[float]] = ...) -> None: ...

class Function(_message.Message):
    __slots__ = ("argtypes", "argnames", "outtypes")
    ARGTYPES_FIELD_NUMBER: _ClassVar[int]
    ARGNAMES_FIELD_NUMBER: _ClassVar[int]
    OUTTYPES_FIELD_NUMBER: _ClassVar[int]
    argtypes: _containers.RepeatedScalarFieldContainer[str]
    argnames: _containers.RepeatedScalarFieldContainer[str]
    outtypes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, argtypes: _Optional[_Iterable[str]] = ..., argnames: _Optional[_Iterable[str]] = ..., outtypes: _Optional[_Iterable[str]] = ...) -> None: ...

class LValue(_message.Message):
    __slots__ = ("type", "inputtype")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INPUTTYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    inputtype: str
    def __init__(self, type: _Optional[str] = ..., inputtype: _Optional[str] = ...) -> None: ...

class ROnly(_message.Message):
    __slots__ = ("type",)
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: str
    def __init__(self, type: _Optional[str] = ...) -> None: ...

class Identifier(_message.Message):
    __slots__ = ("name", "doc", "l", "r", "f")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DOC_FIELD_NUMBER: _ClassVar[int]
    L_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    F_FIELD_NUMBER: _ClassVar[int]
    name: str
    doc: str
    l: LValue
    r: ROnly
    f: Function
    def __init__(self, name: _Optional[str] = ..., doc: _Optional[str] = ..., l: _Optional[_Union[LValue, _Mapping]] = ..., r: _Optional[_Union[ROnly, _Mapping]] = ..., f: _Optional[_Union[Function, _Mapping]] = ...) -> None: ...

class MumaxObject(_message.Message):
    __slots__ = ("name", "ptr")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PTR_FIELD_NUMBER: _ClassVar[int]
    name: str
    ptr: int
    def __init__(self, name: _Optional[str] = ..., ptr: _Optional[int] = ...) -> None: ...

class MumaxObjects(_message.Message):
    __slots__ = ("s",)
    S_FIELD_NUMBER: _ClassVar[int]
    s: _containers.RepeatedCompositeFieldContainer[MumaxObject]
    def __init__(self, s: _Optional[_Iterable[_Union[MumaxObject, _Mapping]]] = ...) -> None: ...

class FunctionCall(_message.Message):
    __slots__ = ("name", "argString", "argBool", "argDouble", "argInt", "argMumax", "argScalarFunction", "argVectorFunction")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ARGSTRING_FIELD_NUMBER: _ClassVar[int]
    ARGBOOL_FIELD_NUMBER: _ClassVar[int]
    ARGDOUBLE_FIELD_NUMBER: _ClassVar[int]
    ARGINT_FIELD_NUMBER: _ClassVar[int]
    ARGMUMAX_FIELD_NUMBER: _ClassVar[int]
    ARGSCALARFUNCTION_FIELD_NUMBER: _ClassVar[int]
    ARGVECTORFUNCTION_FIELD_NUMBER: _ClassVar[int]
    name: str
    argString: _containers.RepeatedScalarFieldContainer[str]
    argBool: _containers.RepeatedScalarFieldContainer[bool]
    argDouble: _containers.RepeatedScalarFieldContainer[float]
    argInt: _containers.RepeatedScalarFieldContainer[int]
    argMumax: _containers.RepeatedCompositeFieldContainer[MumaxObject]
    argScalarFunction: _containers.RepeatedCompositeFieldContainer[ScalarFunction]
    argVectorFunction: _containers.RepeatedCompositeFieldContainer[VectorFunction]
    def __init__(self, name: _Optional[str] = ..., argString: _Optional[_Iterable[str]] = ..., argBool: _Optional[_Iterable[bool]] = ..., argDouble: _Optional[_Iterable[float]] = ..., argInt: _Optional[_Iterable[int]] = ..., argMumax: _Optional[_Iterable[_Union[MumaxObject, _Mapping]]] = ..., argScalarFunction: _Optional[_Iterable[_Union[ScalarFunction, _Mapping]]] = ..., argVectorFunction: _Optional[_Iterable[_Union[VectorFunction, _Mapping]]] = ...) -> None: ...

class Array(_message.Message):
    __slots__ = ("i", "b", "s", "d", "o", "a")
    I_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    D_FIELD_NUMBER: _ClassVar[int]
    O_FIELD_NUMBER: _ClassVar[int]
    A_FIELD_NUMBER: _ClassVar[int]
    i: INTs
    b: BOOLs
    s: STRINGs
    d: DOUBLEs
    o: MumaxObjects
    a: Arrays
    def __init__(self, i: _Optional[_Union[INTs, _Mapping]] = ..., b: _Optional[_Union[BOOLs, _Mapping]] = ..., s: _Optional[_Union[STRINGs, _Mapping]] = ..., d: _Optional[_Union[DOUBLEs, _Mapping]] = ..., o: _Optional[_Union[MumaxObjects, _Mapping]] = ..., a: _Optional[_Union[Arrays, _Mapping]] = ...) -> None: ...

class Arrays(_message.Message):
    __slots__ = ("s",)
    S_FIELD_NUMBER: _ClassVar[int]
    s: _containers.RepeatedCompositeFieldContainer[Array]
    def __init__(self, s: _Optional[_Iterable[_Union[Array, _Mapping]]] = ...) -> None: ...

class CallResponse(_message.Message):
    __slots__ = ("outString", "outBool", "outDouble", "outInt", "outMumax", "outArray")
    OUTSTRING_FIELD_NUMBER: _ClassVar[int]
    OUTBOOL_FIELD_NUMBER: _ClassVar[int]
    OUTDOUBLE_FIELD_NUMBER: _ClassVar[int]
    OUTINT_FIELD_NUMBER: _ClassVar[int]
    OUTMUMAX_FIELD_NUMBER: _ClassVar[int]
    OUTARRAY_FIELD_NUMBER: _ClassVar[int]
    outString: _containers.RepeatedScalarFieldContainer[str]
    outBool: _containers.RepeatedScalarFieldContainer[bool]
    outDouble: _containers.RepeatedScalarFieldContainer[float]
    outInt: _containers.RepeatedScalarFieldContainer[int]
    outMumax: _containers.RepeatedCompositeFieldContainer[MumaxObject]
    outArray: _containers.RepeatedCompositeFieldContainer[Array]
    def __init__(self, outString: _Optional[_Iterable[str]] = ..., outBool: _Optional[_Iterable[bool]] = ..., outDouble: _Optional[_Iterable[float]] = ..., outInt: _Optional[_Iterable[int]] = ..., outMumax: _Optional[_Iterable[_Union[MumaxObject, _Mapping]]] = ..., outArray: _Optional[_Iterable[_Union[Array, _Mapping]]] = ...) -> None: ...

class RevComRequest(_message.Message):
    __slots__ = ("scalarpyfunc", "vectorpyfunc")
    SCALARPYFUNC_FIELD_NUMBER: _ClassVar[int]
    VECTORPYFUNC_FIELD_NUMBER: _ClassVar[int]
    scalarpyfunc: int
    vectorpyfunc: int
    def __init__(self, scalarpyfunc: _Optional[int] = ..., vectorpyfunc: _Optional[int] = ...) -> None: ...

class Vector(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class RevComResult(_message.Message):
    __slots__ = ("scalar", "vec")
    SCALAR_FIELD_NUMBER: _ClassVar[int]
    VEC_FIELD_NUMBER: _ClassVar[int]
    scalar: float
    vec: Vector
    def __init__(self, scalar: _Optional[float] = ..., vec: _Optional[_Union[Vector, _Mapping]] = ...) -> None: ...

class MethodCall(_message.Message):
    __slots__ = ("mmobj", "fc")
    MMOBJ_FIELD_NUMBER: _ClassVar[int]
    FC_FIELD_NUMBER: _ClassVar[int]
    mmobj: MumaxObject
    fc: FunctionCall
    def __init__(self, mmobj: _Optional[_Union[MumaxObject, _Mapping]] = ..., fc: _Optional[_Union[FunctionCall, _Mapping]] = ...) -> None: ...

class MumaxField(_message.Message):
    __slots__ = ("mmobj", "fieldName")
    MMOBJ_FIELD_NUMBER: _ClassVar[int]
    FIELDNAME_FIELD_NUMBER: _ClassVar[int]
    mmobj: MumaxObject
    fieldName: str
    def __init__(self, mmobj: _Optional[_Union[MumaxObject, _Mapping]] = ..., fieldName: _Optional[str] = ...) -> None: ...

class BoolSet(_message.Message):
    __slots__ = ("mmobj", "s")
    MMOBJ_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    mmobj: MumaxObject
    s: bool
    def __init__(self, mmobj: _Optional[_Union[MumaxObject, _Mapping]] = ..., s: bool = ...) -> None: ...

class IntSet(_message.Message):
    __slots__ = ("mmobj", "s")
    MMOBJ_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    mmobj: MumaxObject
    s: int
    def __init__(self, mmobj: _Optional[_Union[MumaxObject, _Mapping]] = ..., s: _Optional[int] = ...) -> None: ...

class DoubleSet(_message.Message):
    __slots__ = ("mmobj", "s")
    MMOBJ_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    mmobj: MumaxObject
    s: float
    def __init__(self, mmobj: _Optional[_Union[MumaxObject, _Mapping]] = ..., s: _Optional[float] = ...) -> None: ...

class StringSet(_message.Message):
    __slots__ = ("mmobj", "s")
    MMOBJ_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    mmobj: MumaxObject
    s: str
    def __init__(self, mmobj: _Optional[_Union[MumaxObject, _Mapping]] = ..., s: _Optional[str] = ...) -> None: ...

class VectorSet(_message.Message):
    __slots__ = ("mmobj", "x", "y", "z")
    MMOBJ_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    mmobj: MumaxObject
    x: float
    y: float
    z: float
    def __init__(self, mmobj: _Optional[_Union[MumaxObject, _Mapping]] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ...) -> None: ...

class ScalarFunction(_message.Message):
    __slots__ = ("scalar", "gocode", "pyfunc")
    SCALAR_FIELD_NUMBER: _ClassVar[int]
    GOCODE_FIELD_NUMBER: _ClassVar[int]
    PYFUNC_FIELD_NUMBER: _ClassVar[int]
    scalar: float
    gocode: str
    pyfunc: int
    def __init__(self, scalar: _Optional[float] = ..., gocode: _Optional[str] = ..., pyfunc: _Optional[int] = ...) -> None: ...

class ScalarFunctionSet(_message.Message):
    __slots__ = ("mmobj", "s")
    MMOBJ_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    mmobj: MumaxObject
    s: ScalarFunction
    def __init__(self, mmobj: _Optional[_Union[MumaxObject, _Mapping]] = ..., s: _Optional[_Union[ScalarFunction, _Mapping]] = ...) -> None: ...

class ScalarFunction3(_message.Message):
    __slots__ = ("x", "y", "z")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    x: ScalarFunction
    y: ScalarFunction
    z: ScalarFunction
    def __init__(self, x: _Optional[_Union[ScalarFunction, _Mapping]] = ..., y: _Optional[_Union[ScalarFunction, _Mapping]] = ..., z: _Optional[_Union[ScalarFunction, _Mapping]] = ...) -> None: ...

class VectorFunction(_message.Message):
    __slots__ = ("gocode", "components", "pyfunc")
    GOCODE_FIELD_NUMBER: _ClassVar[int]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    PYFUNC_FIELD_NUMBER: _ClassVar[int]
    gocode: str
    components: ScalarFunction3
    pyfunc: int
    def __init__(self, gocode: _Optional[str] = ..., components: _Optional[_Union[ScalarFunction3, _Mapping]] = ..., pyfunc: _Optional[int] = ...) -> None: ...

class VectorFunctionSet(_message.Message):
    __slots__ = ("mmobj", "s")
    MMOBJ_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    mmobj: MumaxObject
    s: VectorFunction
    def __init__(self, mmobj: _Optional[_Union[MumaxObject, _Mapping]] = ..., s: _Optional[_Union[VectorFunction, _Mapping]] = ...) -> None: ...

class MumaxSet(_message.Message):
    __slots__ = ("mmobj", "s")
    MMOBJ_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    mmobj: MumaxObject
    s: MumaxObject
    def __init__(self, mmobj: _Optional[_Union[MumaxObject, _Mapping]] = ..., s: _Optional[_Union[MumaxObject, _Mapping]] = ...) -> None: ...

class Slice(_message.Message):
    __slots__ = ("ncomp", "nx", "ny", "nz", "file")
    NCOMP_FIELD_NUMBER: _ClassVar[int]
    NX_FIELD_NUMBER: _ClassVar[int]
    NY_FIELD_NUMBER: _ClassVar[int]
    NZ_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    ncomp: int
    nx: int
    ny: int
    nz: int
    file: str
    def __init__(self, ncomp: _Optional[int] = ..., nx: _Optional[int] = ..., ny: _Optional[int] = ..., nz: _Optional[int] = ..., file: _Optional[str] = ...) -> None: ...

class GPUSlice(_message.Message):
    __slots__ = ("ncomp", "nx", "ny", "nz", "handle")
    NCOMP_FIELD_NUMBER: _ClassVar[int]
    NX_FIELD_NUMBER: _ClassVar[int]
    NY_FIELD_NUMBER: _ClassVar[int]
    NZ_FIELD_NUMBER: _ClassVar[int]
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    ncomp: int
    nx: int
    ny: int
    nz: int
    handle: bytes
    def __init__(self, ncomp: _Optional[int] = ..., nx: _Optional[int] = ..., ny: _Optional[int] = ..., nz: _Optional[int] = ..., handle: _Optional[bytes] = ...) -> None: ...
