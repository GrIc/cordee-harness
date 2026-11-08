"""The harness, run by the launchers cordee/bin/cordee, cordee/bin/ledger and cordee/bin/cockpit as
`python harness <launcher> ...`. See cordee/WORKFLOW.md."""
import os
import signal
import subprocess
import sys

# Run as a folder, Python puts the folder itself on the path: its parent holds the package.
sys.path[0] = os.path.dirname(os.path.abspath(sys.path[0]))

from harness import brief, checks, deploy, hooks, journal, quiz
from harness.doctor import doctor
from harness.drift import touched


def quiet(command):
    """Runs a command and keeps its output short for the agent: one line when it passes, its last 30 lines when it
    fails."""
    # Through sh, which runs scripts as the dev's shell does, and words its own errors. The script goes through the
    # environment: on Windows, Git Bash's runtime does not give back the escaped quotes Python puts on a command line.
    result = subprocess.run(["sh", "-c", "eval $CORDEE_QUIET", "sh", *command],
                            env=dict(os.environ, CORDEE_QUIET='"$@"'), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, status = result.stdout, result.returncode
    if status == 0:
        hidden = out.count(b"\n")
        print(f"ok: {' '.join(command)} ({hidden} lines hidden)")
        return 0
    sys.stdout.flush()
    if out:
        sys.stdout.buffer.write(b"\n".join(out.rstrip(b"\n").split(b"\n")[-30:]) + b"\n")
    print(f"FAIL ({status}): {' '.join(command)}")
    return status


def misuse(text):
    print(text, file=sys.stderr)
    return 2


def cordee_command(args):
    command = args[0] if args else ""
    if command == "hook" and len(args) == 2:
        hooks.hook(args[1])
    elif command == "committed":
        journal.committed()
    elif command == "audit" and len(args) == 3 and args[1] == "--message":
        return checks.audit_staged(args[2])
    elif command == "audit" and len(args) == 3 and args[1] == "--range":
        return checks.audit_range(args[2])
    elif args == ["audit"]:
        return checks.audit_staged()
    elif command == "fingerprint":
        journal.committed()
        journal.reworked()
        os.makedirs(os.path.dirname(quiz.key_path()), exist_ok=True)
        print(f"fingerprint: {quiz.staged()}")
        print("quiz: QUIZ.md")
        print(f"key: {quiz.key_path()}")
    elif command == "install-hook":
        return hooks.install()
    elif command == "deploy" and len(args) == 3:
        return deploy.deploy(args[1], args[2])
    elif command == "deploy" and len(args) == 5 and args[3] == "--forge":
        return deploy.deploy(args[1], args[2], args[4])
    elif command == "touched":
        for module, lines in touched(args[1] if len(args) > 1 else "HEAD"):
            print(f"{module}\t{lines}")
    elif command == "brief":
        brief.brief(args[1] if len(args) > 1 else "")
    elif command == "next":
        brief.next_step()
    elif args == ["hints"]:
        journal.hints()
        # A repo may remove the cockpit's files, as the hooks' lines allow, and keep tokens: true.
        if hooks.tokens_on() and os.path.isfile(os.path.join(os.path.dirname(__file__), "cockpit.py")):
            from harness import cockpit
            cockpit.hints()
    elif command == "quiet" and len(args) > 1:
        return quiet(args[1:])
    elif command == "doctor":
        doctor()
    else:
        return misuse("usage: bash cordee/bin/cordee hook <message-file>\n"
                      "       bash cordee/bin/cordee audit [--message <file> | --range <base>..<tip>]\n"
                      "       bash cordee/bin/cordee fingerprint | install-hook | touched [<commit>] | brief [<module>]\n"
                      "       bash cordee/bin/cordee next | hints | quiet <command>... | doctor\n"
                      "       bash <kit>/template/cordee/bin/cordee deploy <source> <tag> [--forge github|gitlab]")


def ledger_command(args):
    from harness import ledger
    if args == ["record"]:
        ledger.record()
    elif args[:1] == ["sync"] and len(args) <= 2:
        ledger.sync(args[1] if len(args) == 2 else "origin")
    elif args == ["report"]:
        ledger.report()
    else:
        return misuse("usage: bash cordee/bin/ledger record | sync [<remote>] | report")


def cockpit_command(args):
    from harness import cockpit
    if args[:1] == ["usage"] and len(args) == 4:
        cockpit.usage(args[1], int(args[2]), int(args[3]))
    elif args[:1] == ["report"] and len(args) in (2, 4):
        cockpit.report(args[1], *map(int, args[2:]))
    elif args == ["hints"]:
        cockpit.hints()
    else:
        return misuse("usage: bash cordee/bin/cockpit report <repo> [<since> <until>] | hints"
                      " | usage <repo> <since> <until>")


# Paths with accents and LF line ends, whatever the platform; lines in order when stdout and stderr share a file.
for stream in (sys.stdout, sys.stderr):
    stream.reconfigure(encoding="utf-8", newline="\n", line_buffering=True)
# Piped into head, it stops quietly as the shell tools do. Windows has no SIGPIPE.
if hasattr(signal, "SIGPIPE"):
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
launcher, arguments = sys.argv[1], sys.argv[2:]
sys.exit({"cordee": cordee_command, "ledger": ledger_command, "cockpit": cockpit_command}[launcher](arguments))
