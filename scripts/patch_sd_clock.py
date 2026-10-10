"""
Lowers the SD card SPI clock in the vendored InkplateLibrary from 25 MHz to
10 MHz. The SD card shares its SPI bus with the e-paper panel (SHARED_SPI),
and 25 MHz was causing intermittent SD_CARD_ERROR_WRITE_DATA failures
(garbled data-response bytes) during image downloads. The library is pulled
fresh into .pio/libdeps on every build per platformio.ini's `inkplate_lib`
pin, so this patch re-applies on each build rather than editing it in place.
"""

import re
from pathlib import Path

Import("env")

libdeps_dir = Path(env.subst("$PROJECT_LIBDEPS_DIR")) / env.subst("$PIOENV") / "InkplateLibrary" / "src" / "boards"

if libdeps_dir.is_dir():
    for path in libdeps_dir.rglob("*Driver.cpp"):
        text = path.read_text()
        patched = re.sub(r"SD_SCK_MHZ\(25\)", "SD_SCK_MHZ(10)", text)
        if patched != text:
            path.write_text(patched)
            print(f"[patch_sd_clock] {path.relative_to(libdeps_dir)}: SD_SCK_MHZ 25 -> 10")
