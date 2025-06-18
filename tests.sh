#!/usr/bin/env bash

source "$(dirname "$0")/scripts/common.sh"

# Use ldd to fetch the glibc version.
# Can help with diagnosing CI issues.
glibc_version=$(ldd --version | sed -n '1s/([^)]*)//g; s/.* \([0-9]\+\.[0-9]\+\)$/\1/p')
echo "glibc version: $glibc_version"

# Run integration tests
cd "${PWNDBG_ABS_PATH}/tests"

# Support lldb backend
export LLDB_FLAGS='su'
# default flags, s is for loading initializing script for successful loading of the LLDB module,
# u is for unwinding the state on error, to not let tests change settings on errors
export LLDB_VERSION=$(lldb --version | grep -oP 'version \K[0-9]+\.[0-9]+')

$UV_RUN_TEST python3 tests.py $@

exit_code=$?
exit $exit_code
