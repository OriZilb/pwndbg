from __future__ import annotations

import os
import subprocess

from . import get_binary

binary_reference = get_binary("reference-binary.out")
RUN_FILE_TO_USE_PWNDBG_COMMSNDS = [
    f"'file {binary_reference}'",
    "'b main'",
    "r",
]
# for some reason to use pwndbg commands we need to choose and debug a file, the file used here does not matter


def build_lldb_command(commands, run_file_to_use_pwndbg_commands):
    if run_file_to_use_pwndbg_commands:
        command = (
            [os.environ["DEBUGGER_COMMAND"], "--silent", "--commands"]
            + RUN_FILE_TO_USE_PWNDBG_COMMSNDS
            + [f"'{command}'" for command in commands]
            + ["c", "quit", os.environ["COMMAND_LIST_END_DELIMITER"], os.environ["LLDB_FLAGS"]]
        )
    else:
        command = (
            [os.environ["DEBUGGER_COMMAND"], "--silent", "--commands"]
            + [f"'{command}'" for command in commands]
            + ["quit", os.environ["COMMAND_LIST_END_DELIMITER"], os.environ["LLDB_FLAGS"]]
        )
    return " ".join(command)


def run_lldb_command(commands, run_file_to_use_pwndbg_commands):
    return subprocess.run(
        build_lldb_command(commands, run_file_to_use_pwndbg_commands),
        text=True,
        shell=True,
        capture_output=True,
        stdin=subprocess.DEVNULL,
    )
