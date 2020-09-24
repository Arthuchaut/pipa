import random
import string
from pathlib import Path
from pipa.shell import Shell
from pipa.settings import Settings, System


class Virtualenv:
    def __init__(self, shell: Shell):
        self._shell: Shell = shell

    def init(self) -> str:
        vhome: str = Path(Settings.get('venv', 'home'))
        vname: str = f'{Settings.get("project", "name")}-{self._randhash}'
        self._shell.run(f'python -m venv {str(vhome / vname)}')

        return str(vhome / vname)

    @property
    def _randhash(self) -> str:
        return ''.join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )

    def activate(self) -> None:
        cmd: str = f'source {Settings.get("venv", "home")}/bin/activate'

        if Settings.get('core', 'system') is System.WINDOWS:
            cmd = f'{Settings.get("venv", "home")}/Scripts/activate'

        self._shell.run(cmd)

    def deactivate(self) -> None:
        self._shell.run('deactivate')