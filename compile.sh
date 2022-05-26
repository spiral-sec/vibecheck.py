#!/usr/bin/env bash

set -euo pipefail

PY_PATH=$(which python3 || which python)
VENV_PATH="./venv"
SUPPORTED_VERSION=3.9

PIP_PACKAGES=("colorama==0.4.4" "staticx==0.13.6" "pyinstaller==5.1")
SOURCES=("vibecheck.py")

# Compares floating point numbers...i hate bash
fcomp() {
    awk -v n1="${1}" -v n2="${2}" 'BEGIN {if (n1+0<n2+0) exit 0; exit 1}'
}

check_python_version () {
    [ -f ${PY_PATH} ] || { echo "Could not find Python path" && exit 1; }
    PYTHON_VERSION=$(${PY_PATH} --version | cut -d' ' -f2- - | cut -d'.' -f1-2 -)

    echo "[+] Python installation: ${PY_PATH} [${PYTHON_VERSION}]"
    if fcomp ${PYTHON_VERSION} ${SUPPORTED_VERSION}; then
        echo "[!] Unsupported version."
        echo "        Currently supported version: ${SUPPORTED_VERSION}"
        echo "        Current Python version: ${PYTHON_VERSION}"
        exit 1
    fi
}


install_pip_packages () {
    check_python_version

    ${PY_PATH} -m venv ${VENV_PATH}
    source ${VENV_PATH}/bin/activate

    for package in "${PIP_PACKAGES[@]}"; do
        echo "[!] Installing ${package}"
        ${PY_PATH} -m pip install "${package}" >/dev/null
    done
}


compile () {
    OUTPATH="dist/vibecheck"
    TARGET="vibecheck"
    LINUX_DYN_LIB="/usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2"

    pyinstaller -F ${SOURCES} && staticx --strip -l ${LINUX_DYN_LIB} ${OUTPATH} ${TARGET} >/dev/null
}

if [[ -d ${VENV_PATH} ]]; then
        source ${VENV_PATH}/bin/activate
    else
        install_pip_packages
fi

compile

