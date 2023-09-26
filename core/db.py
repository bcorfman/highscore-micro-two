from typing import Any, Dict, Tuple
from sqlmodel import SQLModel, create_engine, Optional, Field
from starlette.config import Config


class HighScore(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    initials: str
    score: int

    def __init__(cls, classname: str, bases: Tuple[type, ...],
                 dict_: Dict[str, Any], **kw: Any) -> None:
        super().__init__(classname, bases, dict_, **kw)
        cls._engine = None

    def __repr__(self) -> str:
        return f"HighScore(id={self.id!r}, initials={self.initials!r}, " + \
               f"score={self.score!r})"

    def create_engine(self):
        starlette_config = Config("env.txt")
        self.engine = create_engine(starlette_config.get("ELEPHANTSQL_URL"),
                                    echo=True)
