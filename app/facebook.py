"""Helper functions for interacting with Meta Graph API.

This module uses the official Graph API endpoints to perform actions
such as listing pages or publishing posts. Network calls are performed
with the ``requests`` library; callers should supply valid Page access
tokens obtained via the Facebook Login OAuth flow.
"""
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Dict, Any, List

GRAPH_API_BASE = "https://graph.facebook.com/v17.0"


class FacebookClient:
    """Very small wrapper around a subset of the Graph API.

    This implementation is intentionally minimal; production systems
    should include extensive error handling and token management.
    """

    def __init__(self, page_access_token: str) -> None:
        self.token = page_access_token

    def _post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """POST ``data`` to ``path`` and return decoded JSON."""
        data["access_token"] = self.token
        body = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request(f"{GRAPH_API_BASE}/{path}", data=body)
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())

    def _get(self, path: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        params = params or {}
        params["access_token"] = self.token
        query = urllib.parse.urlencode(params)
        with urllib.request.urlopen(f"{GRAPH_API_BASE}/{path}?{query}") as resp:
            return json.loads(resp.read().decode())

    # === Page management ==================================================
    def list_pages(self) -> List[Dict[str, Any]]:
        """Return pages manageable by the user.

        In a real implementation the user access token would be required
        to query ``/me/accounts``. For simplicity this function assumes
        that the provided token is already a Page token and returns basic
        metadata for that Page.
        """
        info = self._get("me")
        return [info]

    # === Publishing =======================================================
    def create_text_post(self, page_id: str, message: str) -> Dict[str, Any]:
        """Publish a simple text post to ``page_id``."""
        return self._post(f"{page_id}/feed", {"message": message})

    def upload_photo(self, page_id: str, image_url: str, caption: str | None = None) -> Dict[str, Any]:
        data: Dict[str, Any] = {"url": image_url}
        if caption:
            data["caption"] = caption
        return self._post(f"{page_id}/photos", data)

    def upload_video(self, page_id: str, video_url: str, title: str, description: str) -> Dict[str, Any]:
        data = {"file_url": video_url, "title": title, "description": description}
        return self._post(f"{page_id}/videos", data)

    # === Insights ========================================================
    def page_insights(self, page_id: str, metric: str) -> Dict[str, Any]:
        """Fetch basic insights for a Page."""
        return self._get(f"{page_id}/insights", {"metric": metric})
