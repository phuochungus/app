from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from langserve import add_routes
from fastapi import FastAPI

from rag_redis.chain import chain as rag_redis_chain

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")


add_routes(app, rag_redis_chain, path="/rag-redis")
# Edit this to add the chain you want to add

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
