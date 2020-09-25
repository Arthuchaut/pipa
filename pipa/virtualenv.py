from __future__ import annotations
import random
import string
from pathlib import Path
from pipa.shell import Shell
from pipa.settings import Settings, System


class RandHash:
    @classmethod
    def gen(self, k: int = 8) -> str:
        return ''.join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )


class Virtualenv:
    def __init__(self, shell: Shell = Shell()):
        self._shell: Shell = shell

    @classmethod
    def deploy(cls) -> str:
        vhome: str = Path(Settings.get('venv', 'home'))
        vname: str = f'{Settings.get("project", "name")}-{RandHash.gen()}'

        with Shell() as sh:
            sh.run(f'python -m venv {str(vhome / vname)}')

        return str(vhome / vname)

    def run(self, cmd: str) -> None:
        self._shell.run(cmd)

    def activate(self) -> None:
        cmd: str = f'source {Settings.get("venv", "home")}/bin/activate'

        if Settings.get('core', 'system') == System.WINDOWS:
            cmd = f'{Settings.get("venv", "home")}/Scripts/activate.ps1'

        self.run(cmd)

    def deactivate(self) -> None:
        self.run('deactivate')

    def __enter__(self) -> Virtualenv:
        self.activate()
        return self

    def __exit__(self, type, value, traceback) -> None:
        self.deactivate()
        self._shell.close()


class VirtualenvError(Exception):
    pass