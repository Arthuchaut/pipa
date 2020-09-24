from __future__ import annotations
import subprocess
import sys
import platform
from pipa.settings import Settings


class Shell:
    SHELL: str = (
        'powershell' if platform.system() == 'Windows' else '/bin/bash'
    )
    SEP: str = '; ' if platform.system() == 'Windows' else ' && '

    def __init__(self):
        self._process: subprocess.Popen = None
        self.open()

    def run(self, cmd: str) -> None:
        self._process.stdin.write(
            bytes(f'{cmd}\n', encoding=Settings.get('core', 'encoding'))
        )
        self._process.stdin.flush()

    def open(self) -> None:
        self._process = subprocess.Popen(
            self.SHELL,
            stdin=subprocess.PIPE,
            stdout=sys.stdout,
            stderr=sys.stderr,
        )

    def close(self) -> int:
        self._process.stdin.close()
        self._process.wait()
        return self._process.returncode

    def __enter__(self) -> Shell:
        self.open()
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.close()
