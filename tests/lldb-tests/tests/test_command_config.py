from __future__ import annotations

import re

from . import utils


def test_config():
    result = utils.run_lldb_command(
        ["set context-disasm-lines 8", "config"], run_file_to_use_pwndbg_commands=True
    )
    assert "8 (10)" in result.stdout

    result = utils.run_lldb_command(
        ["set banner-separator #", "theme"], run_file_to_use_pwndbg_commands=True
    )
    assert "'#' ('\u2500')" in result.stdout

    result = utils.run_lldb_command(
        ["set global-max-fast 0x80", "heap-config"], run_file_to_use_pwndbg_commands=True
    )
    assert "'0x80' ('0')" in result.stdout


def test_config_filtering():
    out = utils.run_lldb_command(
        ["config context-disasm-lines"], run_file_to_use_pwndbg_commands=True
    ).stdout.split("\n")

    lines_matched = [re.match(r"Name\s+Documentation\s+Value\s+\(Default\)", line) for line in out]
    assert any(lines_matched)
    line_index = [True if match else False for match in lines_matched].index(True)
    out = out[line_index:]

    assert re.match(r"-+", out[1])
    assert re.match(
        r"context-disasm-lines\s+number of additional lines to print in the disasm context\s+10",
        out[2],
    )
    assert (
        out[3]
        == "You can set a config variable with `set <config-var> <value>`, and read more about it with `help set <config-var>`."
    )
    assert (
        out[4]
        == "You can generate a configuration file using `configfile` - then put it in your .gdbinit after initializing pwndbg."
    )


def test_config_filtering_missing():
    out = utils.run_lldb_command(["config asdasdasdasd"], run_file_to_use_pwndbg_commands=True)
    assert 'No config parameter found with filter "asdasdasdasd"\n' in out.stdout
