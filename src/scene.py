import struct, hashlib

FLAG_UIDS = 2
FLAG_HAS_SCRIPT_CLASS = 8
FLAG_REAL64 = 4
RESERVED_FIELDS = 11
VARIANT_STRING = 5
STRING_NAME = 44

def _u(b, o):
    n = struct.unpack_from("<I", b, o)[0]; o += 4
    s = b[o:o+n-1] if n else b""
    return s, o+n

def _ustr(b, o):
    """Return (text_bytes, new_offset). u32 len(incl. null) + bytes."""
    n = struct.unpack_from("<I", b, o)[0]; o += 4
    return (b[o:o+n-1] if n else b""), o+n

def walk_variant(b, o, real, ver):
    """Walk one rfb-format variant. Return (new_offset, string_spans).
    string_spans: list of (span_start, span_end, text_bytes) for STRING / STRING_NAME values."""
    spans = []
    start = o
    t = struct.unpack_from("<I", b, o)[0]; o += 4
    def rs(n):
        return n*real
    if t == 1: pass                       # NIL
    elif t == 2: o += 4                   # BOOL
    elif t == 3: o += 4                   # INT
    elif t == 4: o += real                # FLOAT (real)
    elif t == 5:                          # STRING
        s, o = _ustr(b, o); spans.append((o-len(s)-1-4, o, s))
    elif t == 10: o += rs(2)              # VECTOR2
    elif t == 11: o += rs(4)              # RECT2
    elif t == 12: o += rs(3)              # VECTOR3
    elif t == 13: o += rs(4)              # PLANE
    elif t == 14: o += rs(4)              # QUATERNION
    elif t == 15: o += rs(6)              # AABB
    elif t == 16: o += rs(9)              # BASIS
    elif t == 17: o += rs(12)             # TRANSFORM3D
    elif t == 18: o += rs(6)              # TRANSFORM2D
    elif t == 20: o += 16                 # COLOR (4 floats)
    elif t == 22:                         # NODE_PATH
        nc, sc = struct.unpack_from("<HH", b, o); o += 4
        sc = sc & 0x7FFF
        if ver < 3: sc += 1
        for _ in range(nc):
            _id, o = _rmap_string(b, o)
        for _ in range(sc):
            _id, o = _rmap_string(b, o)
    elif t == 23: o += 4                  # RID
    elif t == 24:                         # OBJECT
        ot = struct.unpack_from("<I", b, o)[0]; o += 4
        if ot == 0: pass
        elif ot == 1:
            _x, o = _ustr(b, o); _x, o = _ustr(b, o)
        elif ot in (2, 3): o += 4
        else: raise ValueError("bad object type %d" % ot)
    elif t == 26:                         # DICTIONARY
        ln = struct.unpack_from("<I", b, o)[0] & 0x7FFFFFFF; o += 4
        for _ in range(ln):
            o, s = walk_variant(b, o, real, ver); spans += s
            o, s = walk_variant(b, o, real, ver); spans += s
    elif t == 30:                         # ARRAY
        ln = struct.unpack_from("<I", b, o)[0] & 0x7FFFFFFF; o += 4
        for _ in range(ln):
            o, s = walk_variant(b, o, real, ver); spans += s
    elif t == 31:                         # PACKED_BYTE_ARRAY
        ln = struct.unpack_from("<I", b, o)[0]; o += 4 + ln
        o += (-ln) % 4
    elif t == 32: ln = struct.unpack_from("<I", b, o)[0]; o += 4 + 4*ln
    elif t == 33: ln = struct.unpack_from("<I", b, o)[0]; o += 4 + 4*ln
    elif t == 34:                         # PACKED_STRING_ARRAY
        ln = struct.unpack_from("<I", b, o)[0]; o += 4
        for _ in range(ln):
            _x, o = _ustr(b, o)
    elif t == 35: ln = struct.unpack_from("<I", b, o)[0]; o += 4 + 12*ln
    elif t == 36: ln = struct.unpack_from("<I", b, o)[0]; o += 4 + 16*ln
    elif t == 37: ln = struct.unpack_from("<I", b, o)[0]; o += 4 + 8*ln
    elif t == 40: o += 8                  # INT64
    elif t == 41: o += 8                  # DOUBLE
    elif t == 42: pass                    # CALLABLE
    elif t == 43: pass                    # SIGNAL
    elif t == 44:                         # STRING_NAME (identifier: never translate)
        s, o = _ustr(b, o)
    elif t == 45: o += 8                  # VECTOR2I
    elif t == 46: o += 16                 # RECT2I
    elif t == 47: o += 12                 # VECTOR3I
    elif t == 48: ln = struct.unpack_from("<I", b, o)[0]; o += 4 + 8*ln
    elif t == 49: ln = struct.unpack_from("<I", b, o)[0]; o += 4 + 8*ln
    elif t == 50: o += rs(4)              # VECTOR4
    elif t == 51: o += 16                 # VECTOR4I
    elif t == 52: o += rs(16)             # PROJECTION
    elif t == 53: ln = struct.unpack_from("<I", b, o)[0]; o += 4 + 16*ln
    else: raise ValueError("variant type %d at %d" % (t, start))
    return o, spans

def _rmap_string(b, o):
    """A file-string-table reference (u32 id; high bit set => inline)."""
    return _ustr(b, o) if (struct.unpack_from("<I", b, o)[0] & 0x80000000) else (b"", o+4)

def parse_header(d):
    """Return dict with int_resource offset positions (into d) and count, and data_start."""
    assert d[:4] == b"RSRC"
    o = 4
    big_endian, real64, vma, vmi, vfmt = struct.unpack_from("<5I", d, o); o += 20
    _type, o = _u(d, o)
    importmd, = struct.unpack_from("<Q", d, o); o += 8
    flags, = struct.unpack_from("<I", d, o); o += 4
    uid, = struct.unpack_from("<Q", d, o); o += 8
    if flags & FLAG_HAS_SCRIPT_CLASS:
        _sc, o = _u(d, o)
    o += RESERVED_FIELDS*4
    sts, = struct.unpack_from("<I", d, o); o += 4
    for _ in range(sts):
        _s, o = _u(d, o)
    ext, = struct.unpack_from("<I", d, o); o += 4
    for _ in range(ext):
        _t, o = _u(d, o)
        _p, o = _u(d, o)
        if flags & FLAG_UIDS:
            o += 8
    intn, = struct.unpack_from("<I", d, o); o += 4
    offpos = []
    for _ in range(intn):
        _p, o = _u(d, o)
        offpos.append(o)
        o += 8
    return {"flags": flags, "int_count": intn, "offpos": offpos, "data_start": o,
            "ver_fmt": vfmt, "real64": bool(flags & FLAG_REAL64)}

def patch_strings(d, trans):
    """Replace STRING / STRING_NAME variant values found in the resource data; fix
    internal-resource offsets. Returns (new_bytes, delta)."""
    h = parse_header(d)
    real = 8 if h["real64"] else 4
    ver = h["ver_fmt"]
    # Walk resources: type(ustring), prop_count, [name_idx, variant]*
    o = h["data_start"]
    spans = []
    while o < len(d) - 4:
        # stop when we hit the trailing "RSRC" magic
        if d[o:o+4] == b"RSRC":
            break
        _type, o = _ustr(d, o)
        cnt = struct.unpack_from("<I", d, o)[0]; o += 4
        for _ in range(cnt):
            o += 4  # property name index
            o, s = walk_variant(d, o, real, ver)
            spans += s
    reps = []
    for a, b, eb in spans:
        try:
            en = eb.decode("utf-8")
        except Exception:
            continue
        zh = trans.get(en)
        if zh is None:
            continue
        zb = zh.encode("utf-8")
        reps.append((a, b, struct.pack("<I", len(zb)+1) + zb + b"\x00"))
    if not reps:
        return d, 0
    reps.sort()
    out = bytearray()
    prev = 0
    delta = 0
    first_change = reps[0][0]
    for pos, end, target in reps:
        out += d[prev:pos]
        out += target
        delta += len(target) - (end - pos)
        prev = end
    out += d[prev:]
    # fix int_resource offsets located after first_change
    for op in h["offpos"]:
        val = struct.unpack_from("<Q", d, op)[0]
        if val > first_change:
            struct.pack_into("<Q", out, op, val + delta)
    return bytes(out), delta

if __name__ == "__main__":
    import sys
    p = sys.argv[1]
    d = open(p, "rb").read()
    print(parse_header(d))
