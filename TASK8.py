from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, Game

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class GameCreate(BaseModel):
    title: str
    platform: str
    condition: str

@app.post("/games/")
def add_game(game: GameCreate, db: Session = Depends(get_db)):
    db_game = Game(title=game.title, platform=game.platform, condition=game.condition)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game
@app.get("/games/")
def get_games(db: Session = Depends(get_db)):
    return db.query(Game).all()

@app.get("/games/{game_id}")
def get_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

@app.put("/games/{game_id}")
def update_game(game_id: int, game: GameCreate, db: Session = Depends(get_db)):
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    db_game.title = game.title
    db_game.platform = game.platform
    db_game.condition = game.condition
    db.commit()
    db.refresh(db_game)
    return db_game
@app.delete("/games/{game_id}")
def delete_game(game_id: int, db: Session = Depends(get_db)):
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    db.delete(db_game)
    db.commit()
    return {"message": "Game deleted"}