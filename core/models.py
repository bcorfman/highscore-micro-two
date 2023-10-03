from sqlmodel import SQLModel, Field


class HighScoreBase(SQLModel):
    initials: str
    score: int


class HighScore(HighScoreBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class HighScoreCreate(HighScoreBase):
    pass
