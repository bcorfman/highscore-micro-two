from fastapi import Depends, FastAPI
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.sessions import SessionMiddleware

from core.config import starlette_config
from core.db import DBSetup
from core.models import HighScore, HighScoreBase
import uuid

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=uuid.uuid4())
db_setup = DBSetup()


@app.get("/high_scores", response_model=list[HighScoreBase])
async def get_high_scores(session: AsyncSession = Depends(
    db_setup.get_session)):
    result = await session.execute(
        select(HighScore.initials,
               HighScore.score).order_by(HighScore.score.desc()))
    high_scores = result.all()
    return high_scores


@app.post("/add_score", response_model=HighScore)
async def add_score_to_list(initials: str,
                            score: int,
                            session: AsyncSession = Depends(
                                db_setup.get_session)):
    """ Add a new score with initials to a list of high scores,
    sort the list in descending order, and keep only the top 10
    scores in the database.
    Inputs:
    - initials: a string representing the initials of the player who achieved the score.
    - score: an integer representing the score achieved by the player. """
    hs = None
    if len(initials) > 0 and score >= 0:
        result = await session.execute(select(HighScore))
        total_rows = len(result.all())
        hs = HighScore(initials=initials[:3].upper(), score=score)
        session.add(hs)
        await session.commit()
        await session.refresh(hs)
        if total_rows >= 10:
            rows = await session.execute(
                select(HighScore.score).order_by(
                    HighScore.score.desc()).offset(9).limit(1))
            last_score = rows.all()[0][0]
            await session.execute(
                delete(HighScore).where(HighScore.score < last_score))
            await session.commit()
    return hs


@app.post("/clear_scores", response_model=list[HighScoreBase])
async def clear_high_score_list(session: AsyncSession = Depends(
    db_setup.get_session)):
    statement = delete(HighScore)
    result = await session.execute(statement)
    await session.commit()
    result = await session.execute(select(HighScore))
    high_scores = result.all()
    return [
        HighScoreBase(initials=hs.initials, score=hs.score)
        for hs in high_scores
    ]
