from typing import Tuple
from pathlib import Path
from pipa.virtualenv import Virtualenv, VirtualenvError
from pipa.settings import Settings


class Packager:
    _REQUIREMENTS_FILE: Path = Path('requirements.txt')
    _REQUIREMENTS_DEV_FILE: Path = Path('requirements-dev.txt')
    _REQUIREMENTS_LOCK_FILE: Path = Path('requirements.lock')

    @classmethod
    def install(
        cls, *pkgs: Tuple, is_dev: bool = False, root: Path = Path('.')
    ) -> None:
        for pkg in pkgs:
            Virtualenv.run(f'pip install --upgrade {pkg}')
            cls._register(
                root / cls._REQUIREMENTS_DEV_FILE
                if is_dev
                else root / cls._REQUIREMENTS_FILE,
                pkg,
            )

    @classmethod
    def uninstall(cls, *pkgs: Tuple) -> None:
        for pkg in pkgs:
            if not (req_file := cls._find_in_reqs(pkg)):
                raise PackagerError(
                    f'Package: {pkg} not found in requirements files.'
                )

            Virtualenv.run(f'pip uninstall -y {pkg}')
            cls._unregister(req_file, pkg)

    @classmethod
    def _find_in_reqs(cls, pkg: str) -> Path:
        for req_file in [cls._REQUIREMENTS_FILE, cls._REQUIREMENTS_DEV_FILE]:
            for line in req_file.read_text(
                encoding=Settings.get('core', 'encoding')
            ).split('\n'):
                if pkg.lower() == line.lower():
                    return req_file

        return None

    @classmethod
    def lock(cls, root: Path = Path('.')) -> None:
        ...

    @classmethod
    def _unregister(cls, path: Path, pkg: str) -> None:
        req_pkgs: List[str] = path.read_text(
            encoding=Settings.get('core', 'encoding')
        ).split('\n')
        req_pkgs.remove(pkg)
        path.write_text(
            '\n'.join(req_pkgs), encoding=Settings.get('core', 'encoding')
        )

    @classmethod
    def _register(cls, path: Path, pkg: str) -> None:
        with path.open('a', encoding=Settings.get('core', 'encoding')) as fh:
            fh.write(f'{pkg}\n')


class PackagerError(Exception):
    pass