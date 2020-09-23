from typing import Dict, Any
from pathlib import Path
from datetime import datetime
from pipa.settings import Settings


class Template:
    _ENCODING: str = 'utf-8'

    def __init__(self, pname: str, wkdir: Path = Path('.')):
        self._pname: str = pname
        self._wkdir: Path = wkdir

    def deploy(self) -> None:
        self._deploy_item(
            TBlueprint.generate(self._pname, self._pname_cls), self._wkdir
        )

    def _deploy_item(self, item: Dict[str, Any], cur_path: Path) -> None:
        new_path: Path = cur_path / item['name']

        if item['nature'] is ItemNature.DIR:
            new_path.mkdir()
            for child in item['childs']:
                self._deploy_item(child, new_path)
        elif item['nature'] is ItemNature.FILE:
            new_path.write_text(item['content'], encoding=self._ENCODING)

    @property
    def _pname_cls(self) -> str:
        return ''.join([_.capitalize() for _ in self._pname.split('_')])


class ItemNature:
    DIR: int = 0
    FILE: int = 1


class TBlueprint:
    @classmethod
    def generate(cls, pname: str, pname_cls: str) -> Dict[str, Any]:
        return {
            'nature': ItemNature.DIR,
            'name': pname.lower(),
            'childs': [
                {
                    'nature': ItemNature.DIR,
                    'name': pname.lower(),
                    'childs': [
                        {
                            'nature': ItemNature.DIR,
                            'name': 'libs',
                            'childs': [
                                {
                                    'nature': ItemNature.FILE,
                                    'name': f'{pname.lower()}.py',
                                    'content': f'\'\'\'\n@desc    {pname_cls} '
                                    f'class definition.\n@version 0.0.1\n@date    2020-09-22\n@note    '
                                    f'0.0.1 (2020-09-22) : Init file.\n\'\'\'\n\n\nclass '
                                    f'{pname_cls}:\n\t\'\'\'The {pname_cls} '
                                    f'class that is used by the entrypoint file.\'\'\'\n\n\t...\n',
                                },
                                {
                                    'nature': ItemNature.FILE,
                                    'name': 'main.py',
                                    'content': f'\'\'\'\n@desc    Main class definition.\n@version 0.0.1\n'
                                    f'@date    {datetime.now().strftime("%Y-%m-%d")}\n@note    '
                                    f'0.0.1 ({datetime.now().strftime("%Y-%m-%d")}) : Init file.'
                                    f'\n\'\'\'\n\n\nclass Main:\n\t\'\'\'The main class that is '
                                    f'used by the entrypoint file.\'\'\'\n\n\tdef run() -> '
                                    f'None:\n\t\t\'\'\'The main method that is called first '
                                    f'by the entrypoint file.\'\'\'\n\n\t\t...\n',
                                },
                            ],
                        },
                        {
                            'nature': ItemNature.FILE,
                            'name': '__main__.py',
                            'content': f'\'\'\'\n@desc    Entrypoint file.\n@version 0.0.1\n@date    '
                            f'{datetime.now().strftime("%Y-%m-%d")}\n@note    0.0.1 '
                            f'({datetime.now().strftime("%Y-%m-%d")}) : Init file.\n\'\'\'\n\n\n'
                            f'from {pname.lower()}.main import Main\n\nif __name__ == \'__main__\''
                            f':\n\tMain.run()\n',
                        },
                    ],
                },
                {
                    'nature': ItemNature.DIR,
                    'name': 'tests',
                    'childs': [
                        {
                            'nature': ItemNature.FILE,
                            'name': '.gitkeep',
                            'content': '',
                        }
                    ],
                },
                {
                    'nature': ItemNature.FILE,
                    'name': 'README.md',
                    'content': f'# {pname.upper()}',
                },
                {
                    'nature': ItemNature.FILE,
                    'name': '.gitignore',
                    'content': '# Default ignores\n.vscode/\n__pycache__\nvenv/\n',
                },
            ],
        }