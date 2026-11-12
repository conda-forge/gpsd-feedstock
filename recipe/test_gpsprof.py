"""Regressions for CVE-2026-58459 and CVE-2026-60122 on the installed CLI."""

import json
import subprocess


def render(subtype, used):
    records = [
        {"class": "DEVICES", "devices": [{"subtype": subtype}]},
        {"class": "SKY", "satellites": [
            {"PRN": 1, "ss": 40, "az": 80, "el": 15, "used": used},
            {"PRN": 2, "ss": 42, "az": 90, "el": 20, "used": True},
        ]},
    ]
    records.append(records[-1])
    return subprocess.run(
        ["gpsprof", "-r", "-f", "polar"],
        input="".join(json.dumps(record) + "\n" for record in records),
        text=True, capture_output=True, check=True, timeout=30,
    ).stdout


for used in (True, False):
    output = render("ordinary receiver", used)
    assert "ordinary receiver" in output
    assert f"1\t40\t80\t15\t{used}\n" in output

# Inspect generated gnuplot text without executing the injected commands.
output = render('receiver "`echo GPSD_TITLE_INJECTION`"\n', True)
assert "`" not in output
assert r"\042\140echo GPSD_TITLE_INJECTION\140\042" in output

output = render("ordinary receiver", '\nEOD\nsystem("echo GPSD_DATA_INJECTION")\n')
assert "GPSD_DATA_INJECTION" not in output
assert "1\t40\t80\t15\tFalse\n" in output
