import struct

NIL=0; BOOL=1; INT=2; FLOAT=3; STRING=4; VECTOR2=5; VECTOR2I=6; RECT2=7
RECT2I=8; VECTOR3=9; VECTOR3I=10; TRANSFORM2D=11; VECTOR4=12; VECTOR4I=13
PLANE=14; QUATERNION=15; AABB=16; BASIS=17; TRANSFORM3D=18; PROJECTION=19
COLOR=20; STRING_NAME=21; NODE_PATH=22; RID=23; OBJECT=24; CALLABLE=25
SIGNAL=26; DICTIONARY=27; ARRAY=28
PACKED_BYTE_ARRAY=29; PACKED_INT32_ARRAY=30; PACKED_INT64_ARRAY=31
PACKED_FLOAT32_ARRAY=32; PACKED_FLOAT64_ARRAY=33; PACKED_STRING_ARRAY=34
PACKED_VECTOR2_ARRAY=35; PACKED_VECTOR3_ARRAY=36; PACKED_COLOR_ARRAY=37
PACKED_VECTOR4_ARRAY=38

HEADER_TYPE_MASK=0xFF
FLAG64=1<<16
FLAG_OBJECT_AS_ID=1<<16

class V:
    """A decoded variant that remembers its original bytes so unchanged nodes round-trip exactly."""
    __slots__=("type","value","raw","changed")
    def __init__(self,type,value,raw=None,changed=False):
        self.type=type; self.value=value; self.raw=raw; self.changed=changed
    def __repr__(self):
        return f"V({self.type},{self.value!r})"

def _decode_string(b,o):
    strlen=struct.unpack_from("<i",b,o)[0]; o+=4
    pad=(-strlen)%4
    raw=b[o:o+strlen]
    s=raw.decode("utf-8","surrogateescape")
    o+=strlen+pad
    return s,o

def _encode_string(s):
    raw=s.encode("utf-8","surrogateescape")
    pad=(-len(raw))%4
    return struct.pack("<i",len(raw))+raw+b"\x00"*pad

def decode_variant(b,o,end=None):
    """Return (V, new_offset). Recursively decodes; keeps raw spans."""
    start=o
    header=struct.unpack_from("<I",b,o)[0]; o+=4
    t=header & HEADER_TYPE_MASK
    if t==NIL:
        v=V(t,None)
    elif t==BOOL:
        v=V(t,struct.unpack_from("<I",b,o)[0]!=0); o+=4
    elif t==INT:
        if header & FLAG64:
            v=V(t,struct.unpack_from("<q",b,o)[0]); o+=8
        else:
            v=V(t,struct.unpack_from("<i",b,o)[0]); o+=4
    elif t==FLOAT:
        if header & FLAG64:
            v=V(t,struct.unpack_from("<d",b,o)[0]); o+=8
        else:
            v=V(t,struct.unpack_from("<f",b,o)[0]); o+=4
    elif t in (STRING,STRING_NAME,NODE_PATH):
        s,o=_decode_string(b,o); v=V(t,s)
    elif t==VECTOR2:
        v=V(t,None); o=start+4+(16 if header&FLAG64 else 8)
    elif t==VECTOR2I:
        v=V(t,None); o=start+4+8
    elif t==VECTOR3:
        v=V(t,None); o=start+4+(24 if header&FLAG64 else 12)
    elif t==VECTOR3I:
        v=V(t,None); o=start+4+12
    elif t==VECTOR4:
        v=V(t,None); o=start+4+(32 if header&FLAG64 else 16)
    elif t==VECTOR4I:
        v=V(t,None); o=start+4+16
    elif t==COLOR:
        v=V(t,None); o=start+4+16
    elif t==RECT2:
        v=V(t,None); o=start+4+(32 if header&FLAG64 else 16)
    elif t==RECT2I:
        v=V(t,None); o=start+4+16
    elif t in (PLANE,QUATERNION):
        v=V(t,None); o=start+4+(32 if header&FLAG64 else 16)
    elif t in (AABB,TRANSFORM2D):
        v=V(t,None); o=start+4+(64 if header&FLAG64 else 32)
    elif t in (BASIS,TRANSFORM3D,PROJECTION):
        size={BASIS:9,TRANSFORM3D:12,PROJECTION:16}[t]
        v=V(t,None); o=start+4+size*(8 if header&FLAG64 else 4)
    elif t==ARRAY:
        # typed array kind in bits16-17
        kind=(header>>16)&0b11
        if kind==1:
            o+=4  # builtin type id
        elif kind==2:
            _,o=_decode_string(b,o)
        elif kind==3:
            _,o=_decode_string(b,o)
        count=struct.unpack_from("<I",b,o)[0]&0x7FFFFFFF; o+=4
        elems=[]
        for _ in range(count):
            e,o=decode_variant(b,o,end); elems.append(e)
        v=V(t,elems)
    elif t==DICTIONARY:
        kindk=(header>>16)&0b11; kindv=(header>>18)&0b11
        for k in (kindk,kindv):
            if k==1: o+=4
            elif k in (2,3): _,o=_decode_string(b,o)
        count=struct.unpack_from("<I",b,o)[0]&0x7FFFFFFF; o+=4
        items=[]
        for _ in range(count):
            k,o=decode_variant(b,o,end); val,o=decode_variant(b,o,end)
            items.append((k,val))
        v=V(t,items)
    elif t==PACKED_BYTE_ARRAY:
        n=struct.unpack_from("<I",b,o)[0]; o+=4; v=V(t,bytes(b[o:o+n])); o+=n
    elif t==PACKED_INT32_ARRAY:
        n=struct.unpack_from("<I",b,o)[0]; o+=4; v=V(t,list(struct.unpack_from(f"<{n}i",b,o))); o+=4*n
    elif t==PACKED_INT64_ARRAY:
        n=struct.unpack_from("<I",b,o)[0]; o+=4; v=V(t,list(struct.unpack_from(f"<{n}q",b,o))); o+=8*n
    elif t==PACKED_FLOAT32_ARRAY:
        n=struct.unpack_from("<I",b,o)[0]; o+=4; v=V(t,list(struct.unpack_from(f"<{n}f",b,o))); o+=4*n
    elif t==PACKED_FLOAT64_ARRAY:
        n=struct.unpack_from("<I",b,o)[0]; o+=4; v=V(t,list(struct.unpack_from(f"<{n}d",b,o))); o+=8*n
    elif t==PACKED_STRING_ARRAY:
        n=struct.unpack_from("<I",b,o)[0]; o+=4; arr=[]
        for _ in range(n):
            s,o=_decode_string(b,o); arr.append(s)
        v=V(t,arr)
    elif t==PACKED_VECTOR2_ARRAY:
        n=struct.unpack_from("<I",b,o)[0]; o+=4; sz=8 if header&FLAG64 else 8; o+=n*sz; v=V(t,None)
    elif t==PACKED_VECTOR3_ARRAY:
        n=struct.unpack_from("<I",b,o)[0]; o+=4; o+=n*(24 if header&FLAG64 else 12); v=V(t,None)
    elif t==PACKED_COLOR_ARRAY:
        n=struct.unpack_from("<I",b,o)[0]; o+=4; o+=n*16; v=V(t,None)
    elif t==PACKED_VECTOR4_ARRAY:
        n=struct.unpack_from("<I",b,o)[0]; o+=4; o+=n*(32 if header&FLAG64 else 16); v=V(t,None)
    elif t==RID:
        v=V(t,None); o+=8
    else:
        raise ValueError(f"unsupported variant type {t} at {start}")
    v.raw=bytes(b[start:o])
    return v,o

def encode_variant(v):
    if v.raw is not None and not v.changed:
        return v.raw
    t=v.type
    if t in (STRING,STRING_NAME,NODE_PATH):
        return struct.pack("<I",t)+_encode_string(v.value)
    if t==NIL: return struct.pack("<I",t)
    if t==BOOL: return struct.pack("<I",t)+struct.pack("<I",1 if v.value else 0)
    if t==INT:
        # preserve width from raw if available
        if v.raw and len(v.raw)==12: return struct.pack("<Iq",t,v.value)
        return struct.pack("<Ii",t,v.value)
    if t==FLOAT:
        if v.raw and len(v.raw)==12: return struct.pack("<Id",t,v.value)
        return struct.pack("<If",t,v.value)
    if t==ARRAY:
        out=bytearray(struct.pack("<I",t))
        out+=struct.pack("<I",len(v.value))
        for e in v.value: out+=encode_variant(e)
        return bytes(out)
    if t==DICTIONARY:
        out=bytearray(struct.pack("<I",t))
        out+=struct.pack("<I",len(v.value))
        for k,val in v.value:
            out+=encode_variant(k); out+=encode_variant(val)
        return bytes(out)
    if t==PACKED_STRING_ARRAY:
        out=bytearray(struct.pack("<II",t,len(v.value)))
        for s in v.value: out+=_encode_string(s)
        return bytes(out)
    # fallback: unchanged raw only
    if v.raw is not None: return v.raw
    raise ValueError(f"cannot encode type {t}")
