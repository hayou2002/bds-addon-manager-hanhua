"""BDS Addon Manager 一键汉化补丁。

读取原版 exe，就地重写它内嵌的 Godot 资源包（.pck）：
  * 翻译编译后的 GDScript 字节码（.gdc）里的界面文案；
  * 翻译二进制场景（.scn）里的界面文案。

用法：
    python patch.py <原版exe> [输出exe] [--dry-run]

不指定输出路径时，默认生成同目录下的「<原名> 汉化版.exe」。
"""
import sys, os, argparse
from gdc import GDC
from gvariant import STRING, STRING_NAME, PACKED_STRING_ARRAY
import scene
import pckbuild
from translations import TRANS, SKIP_SCRIPT_FILES

def translate_gdc(blob, relpath):
    g = GDC(blob)
    changed = False
    for v in g.constants:
        if isinstance(v.value, str) and v.value in TRANS:
            new = TRANS[v.value]
            if new != v.value:
                v.value = new
                v.changed = True
                changed = True
    if not changed:
        return None
    return g.compressed()

def translate_scn(blob, relpath):
    new, delta = scene.patch_strings(blob, TRANS)
    return new if delta != 0 else None

def main():
    ap = argparse.ArgumentParser(description="BDS Addon Manager 汉化补丁")
    ap.add_argument("input", help="原版 BDS Addon Manager.exe 路径")
    ap.add_argument("output", nargs="?", help="输出 exe 路径（默认：同目录『xxx 汉化版.exe』）")
    args = ap.parse_args()
    src = args.input
    dst = args.output
    if not dst:
        base, ext = os.path.splitext(src)
        dst = base + " 汉化版" + (ext or ".exe")
    pack = pckbuild.load_pack(src)
    new_content = {}
    for e in pack["entries"]:
        p = e["path"]
        if p.endswith(".gdc") and p not in SKIP_SCRIPT_FILES:
            r = translate_gdc(pack["content"][p], p)
            if r is not None:
                new_content[p] = r
        elif p.endswith(".scn"):
            r = translate_scn(pack["content"][p], p)
            if r is not None:
                new_content[p] = r
    pckbuild.write_exe(pack, dst, new_content)
    print(f"patched {len(new_content)} files -> {dst}")
    for k in sorted(new_content):
        print("  ", k)

if __name__ == "__main__":
    main()
