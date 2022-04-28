cd $SRC_DIR

export CCVERSION="0"

scons -c
scons
scons install prefix=$PREFIX
