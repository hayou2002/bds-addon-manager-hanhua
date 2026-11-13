import struct, hashlib, os

PCK_BASE_DEFAULT = 0x6844200

def find_pck_base(data):
    # PE section named "pck"
    pe = struct.unpack_from("<I", data, 0x3c)[0]
    assert data[pe:pe+4] == b"PE\x00\x00"
    nsec = struct.unpack_from("<H", data, pe+6)[0]
    opt = struct.unpack_from("<H", data, pe+20)[0]
    sec_table = pe + 24 + opt
    for i in range(nsec):
        base = sec_table + i*40
        name = data[base:base+8].rstrip(b"\x00")
        if name == b"pck":
            return base, struct.unpack_from("<I", data, base+20)[0]
    raise ValueError("no pck section")

def load_pack(exe):
    data = open(exe, "rb").read()
    sechdr, pck_base = find_pck_base(data)
    assert data[pck_base:pck_base+4] == b"GDPC"
    ver, maj, mnm, pat, flags = struct.unpack_from("<IIIII", data, pck_base+4)
    file_base, dir_off = struct.unpack_from("<QQ", data, pck_base+24)
    seg = data[pck_base:]
    o = dir_off  # pck-relative
    count = struct.unpack_from("<I", seg, o)[0]; o += 4
    entries = []
    for i in range(count):
        sl = struct.unpack_from("<I", seg, o)[0]; o += 4
        path = seg[o:o+sl].split(b"\x00")[0].decode("utf-8"); o += sl
        ofs, size = struct.unpack_from("<QQ", seg, o); o += 16
        md5 = bytes(seg[o:o+16]); o += 16
        fl = struct.unpack_from("<I", seg, o)[0]; o += 4
        entries.append({"path": path, "ofs": ofs, "size": size, "md5": md5, "flags": fl})
    hdr = {"ver": ver, "maj": maj, "min": mnm, "patch": pat, "flags": flags,
           "file_base": file_base, "dir_off": dir_off}
    fp = lambda e: bytes(seg[file_base + e["ofs"]: file_base + e["ofs"] + e["size"]])
    return {"exe": exe, "pck_base": pck_base, "sechdr": sechdr, "hdr": hdr,
            "entries": entries, "content": {e["path"]: fp(e) for e in entries}}

def build_pack(pack, new_content=None, extra_files=None):
    """new_content: dict path->bytes overriding originals. extra_files: list of (path, bytes)."""
    hdr = pack["hdr"]
    entries = pack["entries"]
    content = dict(pack["content"])
    if new_content:
        content.update(new_content)
    order = list(entries)
    if extra_files:
        for pth, _ in extra_files:
            order.append({"path": pth, "ofs": None, "size": None, "md5": None, "flags": 0})
    file_base = 112
    out_data = bytearray()
    offset_of = {}
    layout = sorted(order, key=lambda e: (e["ofs"] is None, e["ofs"] if e["ofs"] is not None else (1 << 62)))
    for e in layout:
        blob = content[e["path"]] if e["path"] in content else dict(extra_files)[e["path"]]
        out_data += b"\x00" * ((-len(out_data)) % 16)
        offset_of[e["path"]] = len(out_data)
        out_data += blob
    out_data += b"\x00" * ((-len(out_data)) % 16)
    new_entries = []
    for e in order:
        blob = content[e["path"]] if e["path"] in content else dict(extra_files)[e["path"]]
        new_entries.append({"path": e["path"], "ofs": offset_of[e["path"]], "size": len(blob),
                            "md5": hashlib.md5(blob).digest(), "flags": e["flags"]})
    all_paths = [e["path"] for e in new_entries]
    assert len(all_paths) == len(set(all_paths)), "duplicate paths"
    dir_off = file_base + len(out_data)  # pck-relative
    # directory
    d = bytearray()
    d += struct.pack("<I", len(new_entries))
    for e in new_entries:
        pb = e["path"].encode("utf-8")
        pad = (4 - len(pb) % 4) % 4
        d += struct.pack("<I", len(pb)+pad)
        d += pb + b"\x00"*pad
        d += struct.pack("<QQ", e["ofs"], e["size"])
        d += e["md5"]
        d += struct.pack("<I", e["flags"])
    header = bytearray(112)
    header[0:4] = b"GDPC"
    struct.pack_into("<IIIII", header, 4, hdr["ver"], hdr["maj"], hdr["min"], hdr["patch"], hdr["flags"])
    struct.pack_into("<Q", header, 24, file_base)
    struct.pack_into("<Q", header, 32, dir_off)
    pck = bytes(header) + bytes(out_data) + bytes(d)
    pad = (-len(pck)) % 4
    pck += b"\x00" * pad
    footer = struct.pack("<Q", len(pck)) + b"GDPC"
    return pck, footer, new_entries

def write_exe(pack, out_path, new_content=None, extra_files=None):
    data = open(pack["exe"], "rb").read()
    pck, footer, new_entries = build_pack(pack, new_content, extra_files)
    out = bytearray(data[:pack["pck_base"]]) + pck + footer
    # update PE pck section SizeOfRawData (+16) only; leave VirtualSize/SizeOfImage as-is
    sh = pack["sechdr"]
    struct.pack_into("<I", out, sh+16, len(pck)+12)
    with open(out_path, "wb") as f:
        f.write(out)
    return new_entries
