import struct
from compression import zstd
from gvariant import decode_variant, encode_variant

TOKEN_BYTE_MASK=0x80

class GDC:
    def __init__(self, data, path=None):
        self.path=path
        self.raw=data
        i=data.find(b"GDSC")
        assert i>=0, "no GDSC"
        self.magic_off=i
        self.version=struct.unpack_from("<I",data,i+4)[0]
        self.dsize=struct.unpack_from("<I",data,i+8)[0]
        body=data[i+12:]
        if self.dsize==0:
            buf=body
        else:
            buf=zstd.decompress(body)
            assert len(buf)==self.dsize
        self.buf=buf
        self._parse()

    def _parse(self):
        b=self.buf
        self.ident_count,self.const_count,self.tline_count,self.token_count=struct.unpack_from("<4I",b,0)
        o=16
        self.identifiers=[]  # list of str
        for _ in range(self.ident_count):
            ln=struct.unpack_from("<I",b,o)[0]; o+=4
            chars=[]
            for j in range(ln):
                t=bytes(x^0xb6 for x in b[o+j*4:o+j*4+4])
                chars.append(struct.unpack("<I",t)[0])
            o+=ln*4
            self.identifiers.append("".join(chr(c) for c in chars))
        self.constants=[]  # list of V
        for _ in range(self.const_count):
            v,o=decode_variant(b,o)
            self.constants.append(v)
        self.tables_start=o
        self.tail=b[o:]  # token_lines + token_columns + tokens, copied verbatim

    def encode(self):
        out=bytearray()
        out+=struct.pack("<4I",self.ident_count,self.const_count,self.tline_count,self.token_count)
        for s in self.identifiers:
            cps=[ord(c) for c in s]
            out+=struct.pack("<I",len(cps))
            for cp in cps:
                raw=struct.pack("<I",cp)
                out+=bytes(x^0xb6 for x in raw)
        for v in self.constants:
            out+=encode_variant(v)
        out+=self.tail
        return bytes(out)

    def compressed(self):
        buf=self.encode()
        comp=zstd.compress(buf)
        return self.raw[:self.magic_off]+b"GDSC"+struct.pack("<II",self.version,len(buf))+comp

def load(path):
    return GDC(open(path,"rb").read(), path)

if __name__=="__main__":
    import sys,glob
    root=r"D:\AI\OH-Workspace\projects\bds-addon-hanhua\work\unpacked"
    import os
    for f in sorted(glob.glob(os.path.join(root,"**","*.gdc"),recursive=True)):
        g=GDC(open(f,"rb").read())
        # sanity: re-encode matches
        ok = (g.encode()==g.buf)
        print(os.path.relpath(f,root), "ids",g.ident_count,"consts",g.const_count,"roundtrip",ok)
