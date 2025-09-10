# Facebook Page Scheduler (Prototype)

This repository contains a **very small prototype** of a web service that
interacts with the [Meta Graph API](https://developers.facebook.com/docs/graph-api/)
to schedule and publish posts to Facebook Pages. It is **not** a
complete product but demonstrates the core building blocks:

* Wrapper around Graph API for text, photo and video posts.
* In-memory job scheduler for deferred publishing.
* `FastAPI` application with endpoints for listing pages, creating posts
  and scheduling them.

## Running locally

```bash
pip install -r requirements.txt  # requires internet access
uvicorn app.main:app --reload
```

## Tests

The project uses `unittest` for basic syntax checks:

```bash
python -m unittest
```

## Disclaimer

This code is for educational purposes and **omits many production
features** such as OAuth flows, persistent storage, background workers,
webhook handling and comprehensive error checking. Refer to the Meta
Platform Policies and Graph API documentation before using it in a real
project.
