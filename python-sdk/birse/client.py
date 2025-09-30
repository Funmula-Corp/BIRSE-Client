import io
import json
from pathlib import Path
from typing import Optional, Dict, Any, Union, BinaryIO

import requests
from PIL import Image

from .exceptions import BirseAPIError, BirseConnectionError
from .models import SearchResponse, SearchResult


class BirseClient:
    """BIRSE Visual Search API Client"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://birse-image-insight.biggo.com/api",
        timeout: int = 30,
    ):
        """
        Initialize BIRSE client.

        Args:
            api_key: Your BIRSE API key
            base_url: Base URL for the API (optional)
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": api_key,
        })

    def search_by_image(
        self,
        image: Union[str, Path, bytes, BinaryIO],
        max_results: Optional[int] = None,
        min_score: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SearchResponse:
        """
        Search for similar images using an image file.

        Args:
            image: Image file path, bytes, or file-like object
            max_results: Maximum number of results to return
            min_score: Minimum similarity score (0-1)
            metadata: Additional metadata for filtering

        Returns:
            SearchResponse object with search results
        """
        files = {}
        data = {}

        if isinstance(image, (str, Path)):
            image_path = Path(image)
            if not image_path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
            files["image"] = ("image.jpg", open(image_path, "rb"), "image/jpeg")
        elif isinstance(image, bytes):
            files["image"] = ("image.jpg", io.BytesIO(image), "image/jpeg")
        else:
            files["image"] = ("image.jpg", image, "image/jpeg")

        if max_results is not None:
            data["maxResults"] = str(max_results)
        
        if min_score is not None:
            data["minScore"] = str(min_score)
        
        if metadata:
            data["metadata"] = json.dumps(metadata)

        try:
            response = self.session.post(
                f"{self.base_url}/search",
                files=files,
                data=data,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return SearchResponse.from_dict(response.json())
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError):
                raise BirseAPIError(f"API error: {e.response.text}")
            else:
                raise BirseConnectionError(f"Connection error: {str(e)}")
        finally:
            if isinstance(files.get("image"), tuple) and hasattr(files["image"][1], "close"):
                files["image"][1].close()

    def search_by_url(
        self,
        image_url: str,
        max_results: Optional[int] = None,
        min_score: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SearchResponse:
        """
        Search for similar images using an image URL.

        Args:
            image_url: URL of the image to search
            max_results: Maximum number of results to return
            min_score: Minimum similarity score (0-1)
            metadata: Additional metadata for filtering

        Returns:
            SearchResponse object with search results
        """
        payload = {"url": image_url}

        if max_results is not None:
            payload["maxResults"] = max_results
        
        if min_score is not None:
            payload["minScore"] = min_score
        
        if metadata:
            payload["metadata"] = metadata

        try:
            response = self.session.post(
                f"{self.base_url}/search-by-url",
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return SearchResponse.from_dict(response.json())
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError):
                raise BirseAPIError(f"API error: {e.response.text}")
            else:
                raise BirseConnectionError(f"Connection error: {str(e)}")

    def upload_image(
        self,
        image: Union[str, Path, bytes, BinaryIO],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Upload an image to the BIRSE database.

        Args:
            image: Image file path, bytes, or file-like object
            metadata: Additional metadata to store with the image

        Returns:
            Dict with upload status and image ID
        """
        files = {}
        data = {}

        if isinstance(image, (str, Path)):
            image_path = Path(image)
            if not image_path.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
            files["image"] = ("image.jpg", open(image_path, "rb"), "image/jpeg")
        elif isinstance(image, bytes):
            files["image"] = ("image.jpg", io.BytesIO(image), "image/jpeg")
        else:
            files["image"] = ("image.jpg", image, "image/jpeg")

        if metadata:
            data["metadata"] = json.dumps(metadata)

        try:
            response = self.session.post(
                f"{self.base_url}/upload",
                files=files,
                data=data,
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError):
                raise BirseAPIError(f"API error: {e.response.text}")
            else:
                raise BirseConnectionError(f"Connection error: {str(e)}")
        finally:
            if isinstance(files.get("image"), tuple) and hasattr(files["image"][1], "close"):
                files["image"][1].close()

    def delete_image(self, image_id: str) -> Dict[str, Any]:
        """
        Delete an image from the BIRSE database.

        Args:
            image_id: ID of the image to delete

        Returns:
            Dict with deletion status
        """
        try:
            response = self.session.delete(
                f"{self.base_url}/images/{image_id}",
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError):
                raise BirseAPIError(f"API error: {e.response.text}")
            else:
                raise BirseConnectionError(f"Connection error: {str(e)}")

    def get_status(self) -> Dict[str, Any]:
        """
        Get API status and version information.

        Returns:
            Dict with status information
        """
        try:
            response = self.session.get(
                f"{self.base_url}/status",
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError):
                raise BirseAPIError(f"API error: {e.response.text}")
            else:
                raise BirseConnectionError(f"Connection error: {str(e)}")