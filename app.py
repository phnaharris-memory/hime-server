from fastapi import FastAPI
from routers import lesson
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()
app.include_router(lesson.router)
app.mount("/data", StaticFiles(directory="data"), name="data")


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
