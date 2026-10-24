#!/usr/bin/env python3
"""
Server Lifecycle Test Automation Runner (with_server.py).

Launches one or more background development servers, polls ports until sockets
are ready, executes a test suite or command, and guarantees complete process group
cleanup.
"""

from __future__ import annotations

import argparse
import atexit
import os
import signal
import socket
import subprocess
import sys
import time
from typing import List, Tuple

ACTIVE_PROCESS_GROUPS: List[int] = []


def cleanup_process_groups() -> None:
    """Terminate all tracked process groups cleanly on script exit."""
    killed = False
    for pgid in ACTIVE_PROCESS_GROUPS:
        try:
            os.killpg(pgid, signal.SIGTERM)
            killed = True
        except (ProcessLookupError, PermissionError, OSError):
            pass

    if killed:
        time.sleep(0.1)
        for pgid in ACTIVE_PROCESS_GROUPS:
            try:
                os.killpg(pgid, signal.SIGKILL)
            except (ProcessLookupError, PermissionError, OSError):
                pass


atexit.register(cleanup_process_groups)


def is_port_in_use(port: int, host: str = "127.0.0.1", timeout_sec: float = 0.5) -> bool:
    """Test if a socket is already active and accepting connections."""
    try:
        with socket.create_connection((host, port), timeout=timeout_sec):
            return True
    except (socket.error, ConnectionRefusedError, OSError):
        return False


def is_port_ready(port: int, host: str = "127.0.0.1", timeout_sec: float = 30.0) -> bool:
    """Poll target socket until active or timeout expires."""
    start = time.monotonic()
    while time.monotonic() - start < timeout_sec:
        try:
            with socket.create_connection((host, port), timeout=1.0):
                return True
        except (socket.error, ConnectionRefusedError, OSError):
            time.sleep(0.25)
    return False


def wait_for_servers_ready(
    server_procs: List[Tuple[str, int, subprocess.Popen]],
    host: str = "127.0.0.1",
    timeout_sec: float = 30.0,
) -> bool:
    """
    Poll all ports until sockets are ready, failing fast if any server exits prematurely.
    """
    start = time.monotonic()
    pending = {port: (cmd_str, proc) for cmd_str, port, proc in server_procs}

    while time.monotonic() - start < timeout_sec:
        # 1. Fail-fast: check if any server process died prematurely
        for port, (cmd_str, proc) in list(pending.items()):
            poll_ret = proc.poll()
            if poll_ret is not None:
                print(
                    f"[with_server] Error: Server '{cmd_str}' exited prematurely with code {poll_ret}.",
                    file=sys.stderr,
                )
                return False

        # 2. Check pending ports
        for port in list(pending.keys()):
            try:
                with socket.create_connection((host, port), timeout=0.5):
                    del pending[port]
                    print(f"[with_server] Port {port} is ready!")
            except (socket.error, ConnectionRefusedError, OSError):
                pass

        if not pending:
            return True

        time.sleep(0.1)

    for port in pending:
        print(f"[with_server] Error: Port {port} failed to become active within {timeout_sec}s.", file=sys.stderr)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run test suite wrapped with managed background servers.",
        usage="%(prog)s [--server 'cmd' --port PORT]... [--host HOST] [--timeout SEC] -- <test_command> [args...]",
    )
    parser.add_argument("--server", action="append", dest="servers", default=[], help="Server command to execute in background")
    parser.add_argument("--port", action="append", dest="ports", type=int, default=[], help="Port to poll for readiness")
    parser.add_argument("--host", default="127.0.0.1", help="Host address to poll (default: 127.0.0.1)")
    parser.add_argument("--timeout", type=float, default=30.0, help="Maximum port readiness wait time in seconds (default: 30)")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Test command to run after servers are ready (prefix with --)")

    args = parser.parse_args()

    servers = args.servers or []
    ports = args.ports or []

    test_cmd = args.command
    if test_cmd and test_cmd[0] == "--":
        test_cmd = test_cmd[1:]

    if not test_cmd:
        print("Error: No test command provided after '--'. Example: with_server.py --server 'npm run dev' --port 3000 -- pytest", file=sys.stderr)
        return 2

    if len(servers) != len(ports):
        print(f"Error: Each --server must have a corresponding --port flag. Got {len(servers)} servers, {len(ports)} ports.", file=sys.stderr)
        return 2

    # Pre-occupied port detection
    for port in ports:
        if is_port_in_use(port, host=args.host):
            print(f"[with_server] Error: Port {port} is already in use.", file=sys.stderr)
            return 1

    # Launch background servers
    server_procs: List[Tuple[str, int, subprocess.Popen]] = []
    try:
        for cmd_str, port in zip(servers, ports):
            print(f"[with_server] Spawning background server: {cmd_str} (expecting port {port})...")
            proc = subprocess.Popen(
                cmd_str,
                shell=True,
                preexec_fn=os.setsid,  # Create distinct process group for clean kill
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            server_procs.append((cmd_str, port, proc))
            pgid = os.getpgid(proc.pid)
            ACTIVE_PROCESS_GROUPS.append(pgid)

            # Check if server died immediately
            poll_ret = proc.poll()
            if poll_ret is not None:
                print(f"[with_server] Error: Server '{cmd_str}' exited immediately with code {poll_ret}.", file=sys.stderr)
                return 1

        # Poll all ports for socket readiness
        for port in ports:
            print(f"[with_server] Polling socket readiness for {args.host}:{port} (timeout {args.timeout}s)...")
        if not wait_for_servers_ready(server_procs, host=args.host, timeout_sec=args.timeout):
            return 1

        # Execute test command
        print(f"[with_server] Executing command: {' '.join(test_cmd)}")
        cmd_res = subprocess.run(test_cmd)
        return cmd_res.returncode

    finally:
        print("[with_server] Terminating all background servers...")
        cleanup_process_groups()


if __name__ == "__main__":
    sys.exit(main())
