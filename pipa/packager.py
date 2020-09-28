from typing import List, Tuple
from pathlib import Path
from pipa.virtualenv import Virtualenv, VirtualenvError
from pipa.settings import Settings


class Packager:
    _REQUIREMENTS_FILE: Path = Path('requirements.txt')
    _REQUIREMENTS_DEV_FILE: Path = Path('requirements-dev.txt')
    _REQUIREMENTS_LOCK_FILE: Path = Path('requirements.lock')

    @classmethod
    def install(
        cls,
        *pkgs: Tuple,
        is_dev: bool = False,
        quiet: bool = False,
        root: Path = Path('.'),
    ) -> None:
        for pkg in pkgs:
            Virtualenv.run(f'pip install --upgrade {pkg}', quiet=quiet)
            req_file = (
                root / cls._REQUIREMENTS_DEV_FILE
                if is_dev
                else root / cls._REQUIREMENTS_FILE
            )
            if not cls._find_in_reqs(pkg, req_file):
                cls._register(
                    req_file,
                    pkg,
                )

    @classmethod
    def uninstall(cls, *pkgs: Tuple, quiet: bool = False) -> None:
        for pkg in pkgs:
            if not (
                req_file := cls._find_in_reqs(
                    pkg, cls._REQUIREMENTS_FILE, cls._REQUIREMENTS_DEV_FILE
                )
            ):
                raise PackagerError(
                    f'Package: {pkg} not found in requirements files.'
                )

            Virtualenv.run(f'pip uninstall -y {pkg}', quiet=quiet)
            cls._unregister(req_file, pkg)

    @classmethod
    def req_install(
        cls, with_dev: bool = True, from_lock: bool = False
    ) -> None:
        if from_lock:
            Virtualenv.run(
                f'pip install --upgrade -r {str(cls._REQUIREMENTS_LOCK_FILE)}'
            )
        else:
            Virtualenv.run(
                f'pip install --upgrade -r {str(cls._REQUIREMENTS_FILE)}'
                f'{" -r " + str(cls._REQUIREMENTS_DEV_FILE) if with_dev else ""}'
            )

    @classmethod
    def _find_in_reqs(cls, pkg: str, *req_files: Tuple) -> Path:
        for req_file in req_files:
            if not req_file.exists():
                raise PackagerError(f'{str(req_file)} doesn\'t exists.')

            for line in req_file.read_text(
                encoding=Settings.get('core', 'encoding')
            ).split('\n'):
                if pkg.lower() == line.lower():
                    return req_file

        return None

    @classmethod
    def lock(
        cls,
        with_hashes: bool = True,
        allow_unsafe: bool = True,
        root: Path = Path('.'),
    ) -> None:
        Virtualenv.run(
            f'python -m piptools compile '
            f'--upgrade '
            f'--no-header '
            f'-q '
            f'{"--generate-hashes " if with_hashes else ""}'
            f'{"--allow-unsafe " if allow_unsafe else ""}'
            f'{str(root / cls._REQUIREMENTS_FILE)} '
            f'-o {str(root / cls._REQUIREMENTS_LOCK_FILE)}',
        )

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