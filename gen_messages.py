import git
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("directory")
parser.add_argument("--etiss-arch-riscv-dir", default=None)

args = parser.parse_args()

directory = Path(args.directory)

with open(directory / "fail", "r") as f:
    fail_content = f.readlines()
with open(directory / "pass", "r") as f:
    pass_content = f.readlines()

pass_content = [line.strip() for line in pass_content if len(line.strip()) > 0]
fail_content = [line.strip() for line in fail_content if len(line.strip()) > 0]

err_content = [line for line in fail_content if "etiss error" in line]
fail_content = [line for line in fail_content if "etiss error" not in line]

num_pass = len(pass_content)
num_err = len(err_content)
num_fail = len(fail_content)

if num_err > 0:
    print("::error ::", num_err, "test(s) crashed:", ", ".join(err_content))
if num_fail > 0:
    print("::warning ::", num_fail, "test(s) failed:", ", ".join(fail_content))
if num_pass > 0:
    print("::notice ::", num_pass, "test(s) passed:", ", ".join(pass_content))
