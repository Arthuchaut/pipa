from pathlib import Path
from pipa.packager import Packager
from typing import List, Set
import click

from pipa.pipa import Pipa
from pipa.settings import Settings


class Main:
    _INFO_COLOR: str = 'cyan'
    _SUCCESS_COLOR: str = 'green'
    _ERR_COLOR: str = 'red'

    @click.group(
        help='The Python managing tools based on native pip and venv tools.'
    )
    def run() -> None:
        pass

    @run.command(help='Create a new project.')
    @click.argument('name', required=True, nargs=1, type=str)
    @click.option(
        '--install',
        '-i',
        type=str,
        help='The package to install in the main requirements (can be specified many times).',
    )
    def new(name: str, install: str) -> None:
        try:
            click.secho('Deploying template...', fg=Main._INFO_COLOR)
            Pipa.init_template(name)

            click.secho('Deploying venv...', fg=Main._INFO_COLOR)
            Pipa.init_venv()

            click.secho('Deployed settings...', fg=Main._INFO_COLOR)
            Pipa.init_settings()

            click.secho('Installing basic packages...', fg=Main._INFO_COLOR)
            Pipa.init_requirements()

            click.secho('Initializing git...', fg=Main._INFO_COLOR)
            Pipa.init_git()

            click.secho(
                f'Done! Use: cd {name}/ and having fun!',
                fg=Main._SUCCESS_COLOR,
                bold=True,
            )
        except Exception as e:
            click.secho(e.__str__(), err=True, fg=Main._ERR_COLOR, bold=True)

    @run.command(help='Initialize Pipa in an existing project.')
    def init() -> None:
        try:
            Main._init()
        except Exception as e:
            click.secho(e.__str__(), err=True, fg=Main._ERR_COLOR, bold=True)

        click.secho('Done! Have fun!', fg=Main._SUCCESS_COLOR, bold=True)

    @run.command(
        'install',
        help='Install or upgrade packages. If no package specified, '
        'Pipa will proceed to install from the requirements file(s), '
        'or the locked file if specified.',
    )
    @click.argument(
        'pkgs',
        nargs=-1,
        type=str,
    )
    @click.option(
        '--dev',
        is_flag=True,
        type=bool,
        default=False,
        help='Specify if package is a development dependency.',
    )
    @click.option(
        '--nolock',
        is_flag=True,
        type=bool,
        default=False,
        help='Specify if Pipa should not install the dependencies from the locked file.',
    )
    def install(pkgs: List[str], dev: bool, nolock: bool) -> None:
        try:
            if not pkgs:
                return Main._init(nolock=nolock, dev=dev)

            for pkg in pkgs:
                click.secho(f'Installing {pkg}...', fg=Main._INFO_COLOR)
                Pipa.install(pkg, is_dev=dev)

            click.secho('Locking dependencies...', fg=Main._INFO_COLOR)
            Pipa.lock()
        except Exception as e:
            click.secho(e.__str__(), err=True, fg=Main._ERR_COLOR, bold=True)

    @run.command('remove', help='Uninstall packages.')
    @click.argument('pkgs', required=True, nargs=-1, type=str)
    def uninstall(pkgs: List[str]) -> None:
        for pkg in pkgs:
            click.secho(f'Removing {pkg}...', fg=Main._INFO_COLOR)
            Pipa.uninstall(pkg)

        click.secho('Locking dependencies...', fg=Main._INFO_COLOR)
        Pipa.lock()

    @run.command(
        'run',
        context_settings={'ignore_unknown_options': True},
        help='Run a command through the virtual environment.',
    )
    @click.argument('cmd', required=True, nargs=-1, type=str)
    def exec(cmd: List[str]) -> None:
        click.secho(
            f'Running in {Path(Settings.get("venv", "home")).name} '
            f'environment...',
            fg=Main._INFO_COLOR,
        )
        Pipa.run(' '.join(cmd))

    def _init(nolock: bool = True, dev: bool = False) -> None:
        # If not, consider that the project has not been initialized.
        if not Settings.FILE.exists():
            Settings.set('project', 'name', val=Path('.').resolve().name)
            click.secho('Deploying settings...', fg=Main._INFO_COLOR)
            Pipa.init_settings(root=Path('.'))

            click.secho('Deploying venv...', fg=Main._INFO_COLOR)
            Pipa.init_venv()

            click.secho('Installing basic packages...', fg=Main._INFO_COLOR)
            Pipa.init_requirements(root=Path('.'))

        if nolock or not Packager.REQUIREMENTS_LOCK_FILE.exists():
            has_req: bool = False

            click.secho('Installing requirements...', fg=Main._INFO_COLOR)
            if not Pipa.req_install():
                click.secho('No requirements file found.', fg=Main._INFO_COLOR)
            else:
                has_req = True

            if dev:
                click.secho(
                    'Installing dev requirements...', fg=Main._INFO_COLOR
                )
                if not Pipa.req_install(dev=True):
                    click.secho(
                        'No dev requirements file found.', fg=Main._INFO_COLOR
                    )

            if has_req:
                click.secho('Locking packages...', fg=Main._INFO_COLOR)
                Pipa.lock()
        else:
            click.secho(
                'Installing locked dependencies...', fg=Main._INFO_COLOR
            )
            if not Pipa.req_install(from_lock=True):
                click.secho('No locked file found.', fg=Main._INFO_COLOR)


if __name__ == '__main__':
    Main.run()
