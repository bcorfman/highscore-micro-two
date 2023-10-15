from fastapi import Depends, FastAPI
from sqlalchemy import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.middleware.sessions import SessionMiddleware

from core.config import starlette_config
from core.db import DBSetup
from core.models import HighScore, HighScoreCreate

app = FastAPI()
app.add_middleware(SessionMiddleware,
                   secret_key=starlette_config.get('SECRET_KEY'))
db_setup = DBSetup()


@app.get("/high_scores", response_model=list[HighScore])
async def get_high_scores(session: AsyncSession = Depends(
    db_setup.get_session)):
    result = await session.execute(
        select(HighScore).order_by(HighScore.score.desc()))
    high_scores = result.scalars().all()
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
    if len(initials) > 0 and score >= 0:
        high_scores = await get_high_scores(session)
        new_scores = []
        if high_scores:
            for item in high_scores:
                new_scores.append((item.score, item.initials))
        new_scores.append((score, initials[:3].upper()))
        new_scores.sort(reverse=True)
        await clear_high_score_list()
        score_lst = [
            HighScore(initials=item[1], score=item[0])
            for item in new_scores[:10]
        ]
        session.add_all(score_lst)
        await session.commit()
        await session.refresh(score_lst)
    return await get_high_scores(session)


@app.post("/clear_scores")
async def clear_high_score_list(session: AsyncSession = Depends(
    db_setup.get_session)):
    statement = delete(HighScore)
    result = await session.execute(statement)
    await session.commit()
    result = await session.execute(select(HighScore))
    high_scores = result.scalars().all()
    return [
        HighScore(initials=hs.initials, score=hs.score) for hs in high_scores
    ]
