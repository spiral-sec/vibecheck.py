#!/usr/bin/env bash

set -euo pipefail

PY_PATH=$(which python3 || which python)
VENV_PATH="./venv"

PIP_PACKAGES=("colorama==0.4.4" "staticx==0.13.6" "pyinstaller==5.1")
SOURCES=("vibecheck.py")

install_pip_packages () {
    ${PY_PATH} -m venv ${VENV_PATH}
    source ${VENV_PATH}/bin/activate

    for package in "${PIP_PACKAGES[@]}"; do
        echo "[!] Installing ${package}"
        ${PY_PATH} -m pip install "${package}" >/dev/null
    done
}


cleanup () {
    mv dist/vibecheck . && rm -vrf vibecheck.spec build dist
}

compile () {
    OUTPATH="dist/vibecheck"
    TARGET="vibecheck"
    LINUX_DYN_LIB="/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2"

    pyinstaller -F "${SOURCES[@]}" >/dev/null \
        && staticx --strip -l "${LINUX_DYN_LIB}" "${OUTPATH}" "${TARGET}" >/dev/null
}

if [[ -d "${VENV_PATH}" ]]; then
        source ${VENV_PATH}/bin/activate
    else
        install_pip_packages
fi

compile && cleanup

