"""ASGI entrypoint for local runs and Docker (``uvicorn main:app``)."""

from presentation.app import create_app

app = create_app()
