from pathlib import Path
import sys
from typing import Dict, List
from pipa.virtualenv import Virtualenv
from pipa.template import Template
from pipa.packager import Packager
from pipa.settings import Settings


class Pipa:
    _BASIC_PACKAGES: Dict[str, List[str]] = {
        'dev': ['pytest', 'black', 'pip-tools', 'python-dotenv[cli]']
    }

    @classmethod
    def init_template(cls, pname: str) -> None:
        Settings.set('project', 'name', val=pname)
        Template().deploy()

    @classmethod
    def init_venv(cls) -> None:
        Settings.set(
            'venv',
            "home",
            val=str(
                Path(Settings.get('venv', 'home'))
                / f'{Settings.get("project", "name")}-{Virtualenv.gen_hash()}'
            ),
        )
        Virtualenv.deploy()

    @classmethod
    def init_settings(cls, root: Path = None) -> None:
        Settings.init(root=root or Path(Settings.get('project', 'name')))

    @classmethod
    def init_requirements(cls, root: Path = None) -> None:
        is_dev: bool = False

        for env, pkgs in cls._BASIC_PACKAGES.items():
            for pkg in pkgs:
                if env == 'dev':
                    is_dev = True

                cls.install(
                    pkg,
                    is_dev=is_dev,
                    root=root or Path(Settings.get('project', 'name')),
                )

    @classmethod
    def init_git(cls) -> None:
        Virtualenv.runs(
            f'git init {Settings.get("project", "name")}',
            f'cd {Settings.get("project", "name")}',
            'git add --all',
            'git commit -m \'Initialized project structure\'',
            quiet=True,
        )

    @classmethod
    def run(cls, cmd: str) -> None:
        Virtualenv.run(cmd, with_env=True)

    @classmethod
    def req_install(cls, dev: bool = False, from_lock: bool = False) -> bool:
        return Packager.req_install(dev=dev, from_lock=from_lock)

    @classmethod
    def install(
        cls,
        pkg: str,
        is_dev: bool = False,
        quiet: bool = True,
        root: Path = Path('.'),
    ) -> None:
        Packager.install(pkg, is_dev=is_dev, quiet=quiet, root=root)

    @classmethod
    def uninstall(cls, pkg: str) -> None:
        Packager.uninstall(pkg, quiet=True)

    @classmethod
    def lock(cls) -> None:
        Packager.lock(allow_unsafe=False)

    @classmethod
    def abort(cld) -> None:
        sys.exit(1)
