from typing import List
import click

from pipa.pipa import Pipa


class Main:
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
    def new(name: str, i: str) -> None:
        ...

    @run.command(help='Initialize Pipa in an existing project.')
    def init() -> None:
        ...

    @run.command(
        'install',
        help='Install or upgrade packages. If no package specified, '
        'Pipa will proceed to install from the requirements file(s), '
        'or the locked file if specified.',
    )
    @click.argument(
        'pkgs',
        nargs=-1,
        type=list,
    )
    @click.option(
        '--dev',
        type=bool,
        default=False,
        help='Specify if package is a development dependency.',
    )
    @click.option(
        '--nolock',
        type=bool,
        default=False,
        help='Specify if Pipa should install the dependencies from the locked file.',
    )
    def install(pkgs: List[str], dev: bool) -> None:
        ...

    @run.command('remove', help='Uninstall packages.')
    @click.argument('pkgs', required=True, nargs=-1, type=list)
    def uninstall(pkgs: List[str]) -> None:
        ...

    @run.command('run', help='Run a command through the virtual environment.')
    @click.argument('cmd', required=True, nargs=-1, type=list)
    def exec(cmd: List[str]) -> None:
        ...


if __name__ == '__main__':
    Main.run()
