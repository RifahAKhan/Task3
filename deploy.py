from subprocess import run, check_output
from pathlib import Path
from shutil import copy

build_cmd = ["bazel.exe", "build", "smartModel"]
query_cmd = ["bazel.exe", "cquery", "PackagesmartModel", "--output=files"]

run(build_cmd)
res = check_output(query_cmd).decode('utf-8').strip()

artifact_path = Path(res).absolute()
target_path = Path(".").joinpath(artifact_path.name)

copy(str(artifact_path),str(target_path))