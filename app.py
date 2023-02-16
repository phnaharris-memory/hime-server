from fastapi import FastAPI
from routers import lesson
import uvicorn

app = FastAPI()
app.include_router(lesson.router)


def run_server():
    """Run server."""

    # start the server!
    uvicorn.run(
        "app:app",
        # host='0.0.0.0',
        port=3000,
    )


if __name__ == "__main__":
    run_server()
