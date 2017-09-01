#!/bin/bash
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
OUT_FILE=${SCRIPT_DIR}/rtilogparser
pushd "$SCRIPT_DIR/src"

# Create a zip file with all the python files.
# The python interpreter is able to read zip files and it will execute the
# content from __main__.py
zip -r "${OUT_FILE}.zip" . -i '*.py'
zip -j "${OUT_FILE}.zip" ../LICENSE

echo '#!/usr/bin/env python' | cat - "${OUT_FILE}.zip" > "${OUT_FILE}"
chmod +x "${OUT_FILE}"
rm "${OUT_FILE}.zip"

popd