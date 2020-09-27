from __future__ import annotations
from typing import TextIO, List, Tuple
import sys
import subprocess
from pipa.settings import Settings, System


class _Pipe:
    SYSIN: TextIO = sys.stdin
    SYSOUT: TextIO = sys.stdout
    SYSERR: TextIO = sys.stderr
    SUBPROC: int = subprocess.PIPE


class Shell:
    PIPE: _Pipe = _Pipe

    def __init__(self, stdout: TextIO = PIPE.SYSOUT):
        self._processes: List[str] = []
        self._stdin: TextIO = None
        self._stdout: TextIO = stdout
        self._stderr: TextIO = self.PIPE.SUBPROC

    @property
    def _shexe(self) -> str:
        return (
            'powershell '
            if Settings.get('core', 'system') == System.WINDOWS
            else '/bin/bash '
        )

    @property
    def _sep(self) -> str:
        return (
            '; '
            if Settings.get('core', 'system') == System.WINDOWS
            else ' && '
        )

    @property
    def _cmd(self) -> str:
        return self._shexe + self._sep.join(self._processes)

    def write_process(self, cmd: str) -> Shell:
        self._processes += [cmd]
        return self

    def run(self) -> int:
        process: subprocess.Popen = subprocess.Popen(
            self._cmd,
            stdin=self._stdin,
            stdout=self._stdout,
            stderr=self._stderr,
        )

        if err := process.communicate()[1] \
        .decode(Settings.get('core', 'encoding')) \
        .strip():
            raise ProcessExecError(err)

        return process.returncode


class ProcessExecError(Exception):
    pass
