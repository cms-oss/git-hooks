#!/usr/bin/python3

import re
import subprocess
import sys

REGEX_BRANCH = r"^(?:feat|fix|bug|chore)/(#\d+-)?\S{5,}"
REGEX_MESSAGE = r"^(?:feat|fix|bug|chore)\((\S{3,})\):( #\d{1,})? [\S ]{5,}"

BRANCH_EXCEPTIONS = [
    "main",
]


def get_branch_name():
    return (
        subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        .decode("ascii")
        .strip()
    )


def extract_ref(value: str, regex: str) -> str | None:
    match = re.findall(regex, value)
    if match and match[0]:
        return match[0]


def validate_commit(message: str, branch: str) -> None:
    if branch in BRANCH_EXCEPTIONS:
        raise TypeError(f"""
            \033[93mWARNING: You might not have permissions to push to `{branch}`. Use `git reset HEAD~` to undo this commit, 
            create a proper branch and/or commit message and commit the changes again.\033[0m
        """)

    if not re.match(REGEX_BRANCH, branch):
        raise TypeError(f"""
    \033[91mERROR: Invalid branch name:
    It should match \033[4m{REGEX_BRANCH}\033[0m\033[91m
    Example: \033[4mfeat/#12-git-hooks\033[0m
                        """)

    if not re.match(REGEX_MESSAGE, message):
        raise TypeError(f"""
    \033[91mERROR: Invalid commit name:
    It should match \033[4m{REGEX_MESSAGE}\033[0m\033[91m
    Example: \033[4mfeat(scope): #12 Add commit-msg hook\033[0m
                        """)


def main():
    try:
        message_file = sys.argv[1]
        with open(message_file, "r") as fd:
            message = fd.read()
        validate_commit(message, get_branch_name())
        print("Message validated")
        sys.exit(0)
    except Exception as e:
        print(e.args[-1], file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
