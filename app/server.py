from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from langserve import add_routes

from rag_redis.chain import chain as rag_redis_chain

app = FastAPI()


@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


add_routes(app, rag_redis_chain, path="/rag-redis")
# Edit this to add the chain you want to add

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
