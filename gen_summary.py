import git
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("directory")
parser.add_argument("--etiss-arch-riscv-dir", default=None)
parser.add_argument("--etiss-dir", default=None)
parser.add_argument("--m2isar-dir", default=None)
parser.add_argument("--riscv-tests-dir", default=None)

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

etiss_arch_riscv_ref = "?"
m2isar_ref = "?"
etiss_ref = "?"
riscv_tests_ref = "?"

if args.etiss_arch_riscv_dir:
    repo = git.Repo(args.etiss_arch_riscv_dir)
    etiss_arch_riscv_ref = repo.head.commit.hexsha
    etiss_arch_riscv_url = repo.remotes.origin.url.replace(".git", "")
if args.m2isar_dir:
    repo = git.Repo(args.m2isar_dir)
    m2isar_ref = repo.head.commit.hexsha
    m2isar_url = repo.remotes.origin.url.replace(".git", "")
if args.etiss_dir:
    repo = git.Repo(args.etiss_dir)
    etiss_ref = repo.head.commit.hexsha
    etiss_url = repo.remotes.origin.url.replace(".git", "")
if args.riscv_tests_dir:
    repo = git.Repo(args.riscv_tests_dir)
    riscv_tests_ref = repo.head.commit.hexsha
    riscv_tests_url = repo.remotes.origin.url.replace(".git", "")

print("## Test Report")
print()
print("**Error/Fail/Pass:**", f":exclamation:{num_err} / :x: {num_fail} / :white_check_mark: {num_pass}")
print()
print("### Setup")
print()
print("**Directory:**", f"`{directory}`")
print()
print("**Commits:**")
print()
print("`etiss_arch_riscv`:", f"[`{etiss_arch_riscv_ref}`]({etiss_arch_riscv_url}/commit/{etiss_arch_riscv_ref})")
print("`M2-ISA-R`", f"[`{m2isar_ref}`]({m2isar_url}/commit/{m2isar_ref})")
print("`etiss`:", f"[`{etiss_ref}`]({etiss_url}/commit/{etiss_ref})")
print("`riscv-tests`:", f"[`{riscv_tests_ref}`]({riscv_tests_url}/commit/{riscv_tests_ref})")
print()
print("### Details")
print()
print("**Error :exclamation::**")
print()
print("```")
print("\n".join(err_content))
print("```")
print()
print("**Fail :x: :**")
print()
print("```")
print("\n".join(fail_content))
print("```")
print()
print("**Pass :white_check_mark: :**")
print()
print("```")
print("\n".join(pass_content))
print("```")
