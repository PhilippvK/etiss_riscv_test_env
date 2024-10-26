import git
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("directory")
parser.add_argument("--print-passed", action="store_true")
parser.add_argument("--allow-empty", action="store_true")
parser.add_argument("--allow-fail", action="store_true")

args = parser.parse_args()

directory = Path(args.directory)

with open(directory / "fail.txt", "r") as f:
    fail_content = f.readlines()
with open(directory / "pass.txt", "r") as f:
    pass_content = f.readlines()

pass_content = [line.strip() for line in pass_content if len(line.strip()) > 0]
fail_content = [line.strip() for line in fail_content if len(line.strip()) > 0]

err_content = [line for line in fail_content if "etiss error" in line]
fail_content = [line for line in fail_content if "etiss error" not in line]

num_pass = len(pass_content)
num_err = len(err_content)
num_fail = len(fail_content)

if num_err > 0:
    err_tests = [test.split(":", 1)[0] for test in err_content]
    print("::error ::", num_err, "test(s) crashed:", ", ".join(err_tests))
if num_fail > 0:
    fail_tests = [test.split(":", 1)[0] for test in fail_content]
    print("::warning ::", num_fail, "test(s) failed:", ", ".join(fail_tests))
if num_pass > 0 and args.print_passed:
    pass_tests = [test.split(":", 1)[0] for test in pass_content]
    print("::notice ::", num_pass, "test(s) passed:", ", ".join(pass_tests))

if num_pass + num_fail + num_err == 0:
    assert args.allow_empty, "No test results found"

if num_fail > 0:
    assert args.allow_fail, "Failing tests not allowed"
