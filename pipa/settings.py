from typing import Dict, Any, Tuple
from pathlib import Path
import toml


class Settings:
    _FILE: Path = Path('pipa.toml')
    _DEFAULT_SET: Dict[str, Any] = {
        'project': {'name': 'pipa'},
        'env': {'home': 'venv'},
        'core': {'encoding': 'utf-8'},
    }

    @classmethod
    def init(
        cls,
        settings: Dict[str, Any] = _DEFAULT_SET,
        project_path: Path = Path('.'),
    ) -> str:
        toml.dump(settings, (project_path / cls._FILE).open('w'))

    @classmethod
    def get(
        cls,
        *keys,
        _item: Any = toml.load(_FILE) if _FILE.exists() else _DEFAULT_SET
    ) -> Any:
        return (
            cls.get(*keys[1:], _item=_item[keys[0]])
            if keys and _item
            else _item
        )

    @classmethod
    def set(cls, *keys: Tuple, val: Any) -> None:
        item: Any = cls.get(*keys[:-1])
        item[keys[-1]] = val

        if cls._FILE.exists():
            toml.dump(cls.get(), cls._FILE.open('w'))