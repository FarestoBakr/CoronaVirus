"""FastAPI application providing endpoints for Facebook Page scheduling.

The app exposes a subset of the API surface described in the product
requirements. Function bodies are intentionally short and many advanced
features (such as authentication persistence, media uploads, analytics
and webhooks) are left as exercises for a full implementation.
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .facebook import FacebookClient
from .scheduler import scheduler

app = FastAPI(title="FB Scheduler")


@app.on_event("startup")
def _startup() -> None:
    scheduler.start()


@app.on_event("shutdown")
def _shutdown() -> None:
    scheduler.shutdown()


@app.get("/pages")
def get_pages(page_token: str) -> list[dict]:
    """Return manageable pages for the provided Page access token."""
    fb = FacebookClient(page_token)
    return fb.list_pages()


@app.post("/posts")
def create_text_post(page_id: str, page_token: str, message: str) -> dict:
    fb = FacebookClient(page_token)
    return fb.create_text_post(page_id, message)


@app.post("/posts/{post_id}/schedule")
def schedule_post(post_id: str, seconds_from_now: int) -> dict:
    """Dummy scheduling endpoint that runs a no-op job."""
    scheduler.enqueue(seconds_from_now, lambda: None)
    return {"scheduled": post_id, "run_in": seconds_from_now}
