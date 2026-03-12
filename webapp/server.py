"""
This is the main server entry point for the ToDo list application.

It combines the API defined in `webapp.api` with static file serving for the frontend.
Running this script will start the Uvicorn server for development.
"""
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import the FastAPI app instance from the api module.
# This instance contains all the API routes.
from webapp.api import app


# Mount the 'static' directory, which contains the frontend files (HTML, CSS, JS).
# These files will be served under the '/static' path.
# The path "webapp/static" is relative to the project root where the server is run.
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")


@app.get("/")
async def read_index():
    """
    Serves the main index.html file.
    This is the entry point for the single-page frontend application.
    """
    return FileResponse("webapp/static/index.html")


if __name__ == "__main__":
    # This block allows running the server directly using `python -m webapp.server`.
    # It's intended for development purposes. For production, a proper ASGI server
    # like Gunicorn with Uvicorn workers should be used.
    uvicorn.run(app, host="0.0.0.0", port=8000)
