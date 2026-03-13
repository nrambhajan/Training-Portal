import re
import socket
import paramiko
from typing import Tuple


def verify_task(
    host: str,
    port: int,
    username: str,
    password: str,
    command: str,
    verify_type: str,       # exit_code | contains | regex
    verify_expected: str,   # ignored for exit_code
    timeout: int = 15,
) -> Tuple[bool, str]:
    """
    SSH into host, run command, evaluate result.
    Returns (passed: bool, output: str).
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            banner_timeout=timeout,
            auth_timeout=timeout,
            look_for_keys=False,
            allow_agent=False,
        )
    except socket.timeout:
        return False, "ERROR: Connection timed out. Check server IP and port."
    except paramiko.AuthenticationException:
        return False, "ERROR: SSH authentication failed. Check credentials."
    except Exception as e:
        return False, f"ERROR: Could not connect — {e}"

    try:
        stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
        exit_code = stdout.channel.recv_exit_status()
        out = stdout.read().decode("utf-8", errors="replace").strip()
        err = stderr.read().decode("utf-8", errors="replace").strip()
        combined = (out + "\n" + err).strip()
    except Exception as e:
        client.close()
        return False, f"ERROR: Command execution failed — {e}"
    finally:
        client.close()

    if verify_type == "exit_code":
        passed = exit_code == 0
        return passed, combined or f"(exit code {exit_code})"

    if verify_type == "contains":
        passed = (verify_expected or "").lower() in combined.lower()
        return passed, combined

    if verify_type == "regex":
        try:
            passed = bool(re.search(verify_expected, combined, re.IGNORECASE | re.MULTILINE))
        except re.error as e:
            return False, f"ERROR: Bad regex pattern — {e}"
        return passed, combined

    return False, f"ERROR: Unknown verify_type '{verify_type}'"


def check_output_match(
    submitted: str,
    verify_expected: str,
    verify_type: str,
) -> bool:
    """Grade a pasted command output against expected pattern (no SSH needed)."""
    if verify_type == "contains":
        return (verify_expected or "").lower() in submitted.lower()
    if verify_type == "regex":
        try:
            return bool(re.search(verify_expected, submitted, re.IGNORECASE | re.MULTILINE))
        except re.error:
            return False
    # exact
    return submitted.strip() == verify_expected.strip()
