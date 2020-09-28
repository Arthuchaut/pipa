from __future__ import annotations

import re
import sys
import random
import string
from pathlib import Path
from typing import List, TextIO, Tuple

from pipa.settings import Settings, System
from pipa.shell import ProcessExecError, Shell


class Virtualenv:
    _NOTERR: List[str] = [
        'WARNING: You are using pip version',  # Raised by the pip command
        'The generated requirements file may be rejected by pip install',  # Raised by pip-tools when trying to lock unsafe dependencies
    ]
    _ENV_FILE: Path = Path('.env')

    @classmethod
    def _iserr(cls, err: str) -> bool:
        return not re.match(
            r'^' + '|'.join([_.lower() for _ in cls._NOTERR]), err.lower()
        )

    @classmethod
    def gen_hash(cls, k: int = 8) -> str:
        return ''.join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )

    @classmethod
    def _get_activate_cmd(cls) -> str:
        return (
            f'{Settings.get("venv", "home")}\\Scripts\\activate.ps1'
            if Settings.get('core', 'system') == System.WINDOWS
            else f'source {Settings.get("venv", "home")}/bin/activate'
        )

    @classmethod
    def deploy(cls) -> None:
        sh: Shell = Shell(stdout=Shell.PIPE.SUBPROC)
        sh.write_process(f'python -m venv {str(Settings.get("venv", "home"))}')
        sh.run()

    @classmethod
    def runs(
        cls, *cmds: Tuple, quiet: bool = False, with_env: bool = False
    ) -> Virtualenv:
        cmd: str = Shell.SEP.join(cmds)
        cls.run(cmd, quiet=quiet, with_env=with_env)

    @classmethod
    def run(
        cls, cmd: str, quiet: bool = False, with_env: bool = False
    ) -> Virtualenv:
        stdout: TextIO = Shell.PIPE.SUBPROC if quiet else Shell.PIPE.SYSOUT
        sh: Shell = Shell(stdout=stdout)
        sh.write_process(cls._get_activate_cmd())
        sh.write_process(
            'dotenv run'
        ) if cls._ENV_FILE.exists() and with_env else None
        sh.write_process(cmd)
        sh.write_process('deactivate')

        try:
            sh.run()
        except ProcessExecError as e:
            if cls._iserr(e.__str__()):
                raise VirtualenvError(e)
            if not quiet:
                sys.stdout.write(e.__str__())

        return cls


class VirtualenvError(Exception):
    pass
