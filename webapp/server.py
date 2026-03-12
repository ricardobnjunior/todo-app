import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# This line assumes that a file named `webapp/api.py` exists and
# contains a FastAPI application instance named `app`.
from webapp.api import app

# Mount a directory named 'static' (located in 'webapp/static')
# to the URL path '/static'. This allows serving static files like
# CSS, JavaScript, and images.
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

@app.get("/", include_in_schema=False)
async def read_index():
    """
    This endpoint serves the main HTML file of the frontend application.
    It returns the `index.html` file from the static directory.
    """
    return FileResponse("webapp/static/index.html")

if __name__ == "__main__":
    # This block makes the script runnable.
    # When you run `python -m webapp.server`, this code will execute.
    # It starts a Uvicorn server to host the FastAPI application.
    # host="0.0.0.0" makes the server accessible from other devices on the network.
    uvicorn.run(app, host="0.0.0.0", port=8000)
