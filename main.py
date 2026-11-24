#!/usr/bin/env python3
"""news-23 b114 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys
import zlib

PNG_SIG = b"\x89PNG\r\n\x1a\n"
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576
MIN_IDAT = 1_000


def fail(msg):
    print("main.py: error:", msg, file=sys.stderr)
    return 1


def check_png(data):
    """Validate the PNG header + chunk layout (manual parse via struct)."""
    if len(data) < 8 or data[:8] != PNG_SIG:
        return "bad PNG signature"
    if len(data) < 8 + 8 + 13 + 4:
        return "file too short for IHDR"
    # first chunk: length (4 BE) + type (4) + data (13) + CRC (4)
    (length,) = struct.unpack(">I", data[8:12])
    if data[12:16] != b"IHDR" or length != 13:
        return "first chunk is not a 13-byte IHDR"
    ihdr = data[16:29]
    (w, h, depth, ctype, comp, filt, interlace) = struct.unpack(">IIBBBBB", ihdr)
    if (w, h) != (1024, 1024):
        return "not 1024x1024 (got %dx%d)" % (w, h)
    if depth != 8:
        return "bit depth is not 8"
    if ctype not in (2, 6):
        return "colour type is not 2 or 6"
    if comp != 0 or filt != 0 or interlace != 0:
        return "compression/filter/interlace must be 0"
    crc_stored, = struct.unpack(">I", data[29:33])
    if zlib.crc32(b"IHDR" + ihdr) & 0xFFFFFFFF != crc_stored:
        return "IHDR CRC mismatch"
    # chunk walk: each chunk is 8-byte header (4 length + 4 type) + data + 4 CRC,
    # so the cursor advances 12 + clen bytes per chunk. CRC-checked per chunk.
    pos = 8
    idat_total = 0
    saw_iend = False
    while pos + 8 <= len(data):
        (clen,) = struct.unpack(">I", data[pos:pos + 4])
        ctype_b = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            return "truncated chunk %s" % ctype_b.decode("latin-1", "replace")
        chunk = data[pos + 4:pos + 8 + clen]
        crc_stored, = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])
        if zlib.crc32(chunk) & 0xFFFFFFFF != crc_stored:
            return "CRC mismatch in chunk %s" % ctype_b.decode("latin-1", "replace")
        if ctype_b == b"IDAT":
            if clen == 0:
                return "empty IDAT chunk"
            idat_total += clen
        if ctype_b == b"IEND":
            if clen != 0:
                return "IEND must be 0 bytes"
            if pos + 12 + clen != len(data):
                return "trailing data after IEND"
            saw_iend = True
            break
        pos += 12 + clen
    if not saw_iend:
        return "missing IEND chunk"
    if idat_total < MIN_IDAT:
        return "IDAT payload too small (%d bytes)" % idat_total
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    # guard: reject empty / in-repo / file output dirs
    if not outdir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    outdir_abs = os.path.abspath(outdir)
    if os.path.exists(outdir_abs) and not os.path.isdir(outdir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file: %s" % outdir)
    if os.path.commonpath([outdir_abs, here]) == here:
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo: %s" % outdir)
    dst = os.path.join(outdir_abs, "entry.png")
    # guard: never overwrite the source
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source entry.png")
    if not os.path.isfile(src):
        return fail("source entry.png missing: %s" % src)
    with open(src, "rb") as f:
        data = f.read()
    if len(data) < MIN_BYTES:
        return fail("entry.png too small: %d bytes" % len(data))
    if len(data) > MAX_BYTES:
        return fail("entry.png over 1 MiB: %d bytes" % len(data))
    err = check_png(data)
    if err:
        return fail(err)
    os.makedirs(outdir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    # re-read output: confirm byte-identical
    with open(dst, "rb") as f:
        out = f.read()
    if out != data:
        return fail("output differs from source after write")
    print("entry.png sha256:", hashlib.sha256(data).hexdigest())
    print("wrote", dst, len(data), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
