from fastapi import FastAPI ,request, HTTPException
from fastapi.responses import JSONResponse
import httpx
import os
from slowapi import Limiter
from slowapi.util import get_remote_address
import aioredis
app =Fastapi()
limiter = Limiter( key_func =get_remote_address)
OMDB_API_KEY = "your_api_key"
OMDB_URL = "http://www.omdbapi.com/"
redis = None 
@app.on_event("startup")
async def startup():
    global redis
    redis = await aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)

@app.on_event("shutdown")
async def shutdown():
    await redis.close()

# Custom error handler for rate limiting
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.get("/movie/{movie_name}")
@limiter.limit("5/minute")
async def get_movie(movie_name: str, request: Request):
    """Fetches movie details from OMDb API"""
    async with httpx.AsyncClient() as client:
        response = await client.get(OMDB_URL, params={"t": movie_name, "apikey": OMDB_API_KEY})
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching movie data")

        data = response.json()
        if data.get("Response") == "False":
            raise HTTPException(status_code=404, detail="Movie not found")

        return {
            "id": data.get("imdbID"),
            "title": data.get("Title"),
            "rating": data.get("imdbRating"),
            "image": data.get("Poster")
        }

# Run the app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)        