#!/usr/bin/env bash
set -euo pipefail

# Generate SQLCipher amalgamation (sqlite3.c/sqlite3.h) and copy into build/sqlcipher
# Requires: git, make, cc, tclsh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$ROOT_DIR/build/sqlcipher"
WORK_DIR="${TMPDIR:-/tmp}/sqlcipher-src"

mkdir -p "$BUILD_DIR"

if [ ! -d "$WORK_DIR/.git" ]; then
  rm -rf "$WORK_DIR"
  git clone --depth=1 https://github.com/sqlcipher/sqlcipher "$WORK_DIR"
fi

cd "$WORK_DIR"
# Use generic Makefile to generate sqlite3.c/sqlite3.h
make -f Makefile.linux-generic sqlite3.c

# Copy amalgamation to build dir
cp -f sqlite3.c "$BUILD_DIR/sqlite3.c"
cp -f sqlite3.h "$BUILD_DIR/sqlite3.h"

# Prepend required SQLCipher defines into sqlite3.c to enable codec and crypto backend
# Only add once
if ! grep -q "SQLITE_HAS_CODEC" "$BUILD_DIR/sqlite3.c"; then
  tmpfile="$(mktemp)"
  {
    echo "#ifndef SQLITE_HAS_CODEC"
    echo "#define SQLITE_HAS_CODEC 1"
    echo "#endif"
    echo "#ifndef SQLCIPHER_CRYPTO_CC"
    echo "#define SQLCIPHER_CRYPTO_CC 1"
    echo "#endif"
    echo "#ifndef SQLITE_TEMP_STORE"
    echo "#define SQLITE_TEMP_STORE 2"
    echo "#endif"
    cat "$BUILD_DIR/sqlite3.c"
  } > "$tmpfile"
  mv "$tmpfile" "$BUILD_DIR/sqlite3.c"
fi

echo "SQLCipher amalgamation ready at $BUILD_DIR"
