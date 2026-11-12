set -eux

scons -j"${CPU_COUNT}" prefix="$PREFIX" python_libdir="$SP_DIR"
scons install prefix="$PREFIX" python_libdir="$SP_DIR"
