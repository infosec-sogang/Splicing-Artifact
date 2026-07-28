# Number of containers to run in parallel.
MAX_CONTAINER_NUM = 60
# Memory limitation (in GB) for each container.
MEM_PER_CONTAINER = 4

# Each line represents <program, seed format, cmdline argument, input file>
TARGETS = [
    ("tiff_read_rgba_fuzzer","tiff", "input.tif", "input.tif"),
    ("objdump","elf", "-D input", "input"),
    ("readelf","elf", "-a input", "input"),
    ("cxxfilt", "empty", "", ""),
    ("xml2_read_fuzzer","xml", "input.xml", "input.xml"),
    ("idlc", "idl", "input.idl", "input.idl"),
    ("libpng_read_fuzzer","png","input.png", "input.png"),
    ("tic", "src", "input.src", "input.src"),
    ("infotocap", "dat", "input.dat", "input.dat"),
]
