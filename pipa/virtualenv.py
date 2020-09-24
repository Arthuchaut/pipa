from pipa.shell import Shell
from pipa.settings import Settings, System


class Virtualenv:
    def __init__(self, shell: Shell):
        self._shell: Shell = shell

    def activate(self) -> None:
        cmd: str = 'source venv/bin/activate'

        if Settings.SYSTEM is System.WINDOWS:
            cmd = 'venv/Scripts/activate'

        self._shell.run(cmd)

    def deactivate(self) -> None:
        self._shell.run('deactivate')