import json
from typing import Optional, Dict, Any, List, Tuple

import requests

from .exceptions import BirseAPIError, BirseConnectionError
from .models import SearchResponse


class BirseClient:
    """BIRSE Visual Search API Client for Shopify"""

    def __init__(
        self,
        shop_id: str,
        shop_permanent_domain: str,
        timeout: int = 30,
    ):
        """
        Initialize BIRSE client.

        Args:
            shop_id: Your Shopify shop ID
            shop_permanent_domain: Your shop's permanent domain (e.g., 'your-shop.myshopify.com')
            timeout: Request timeout in seconds (default: 30)
        """
        self.shop_id = shop_id
        self.shop_permanent_domain = shop_permanent_domain
        self.timeout = timeout
        self.session = requests.Session()

    def upload_image(self, image_file: Any) -> Dict[str, Any]:
        """
        Upload an image file to BIRSE.

        Args:
            image_file: Image file object (from file input)

        Returns:
            Dict with result status and image_id
        """
        files = {'image': image_file}
        data = {'shop': self.shop_id}

        try:
            response = self.session.post(
                'https://api.biggo.com/api/v1/shopify/upload_image',
                files=files,
                data=data,
                timeout=self.timeout,
            )
            response.raise_for_status()
            result = response.json()

            if not result.get('result'):
                raise BirseAPIError('Upload failed')
            if not result.get('image_id'):
                raise BirseAPIError('No image id returned')

            return result
        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError):
                raise BirseAPIError(f"API error: {e.response.text}")
            else:
                raise BirseConnectionError(f"Connection error: {str(e)}")

    def search_image(
        self,
        image_id: str,
        xywh: Optional[Tuple[int, int, int, int]] = None,
        metafields: Optional[List[Dict[str, str]]] = None,
        country: Optional[str] = None,
        lang: Optional[str] = None,
    ) -> SearchResponse:
        """
        Search for similar products using an uploaded image ID.

        Args:
            image_id: The image ID from upload_image
            xywh: Optional crop coordinates [x, y, width, height]
            metafields: Optional metafields filters [{'namespace': '...', 'key': '...'}]
            country: Optional country code (e.g., 'US')
            lang: Optional language code (e.g., 'EN')

        Returns:
            SearchResponse with product results
        """
        payload = {
            'image_id': image_id,
            'xywh': list(xywh) if xywh else None,
            'is_orientation': False,
            'shop': self.shop_id
        }

        try:
            similar_ids_res = self.session.post(
                'https://api.biggo.com/api/v1/shopify/similar_image',
                json=payload,
                timeout=self.timeout,
            )
            similar_ids_res.raise_for_status()
            similar_ids = similar_ids_res.json()

            if not isinstance(similar_ids, list) or len(similar_ids) == 0:
                return SearchResponse(result=True, products=[])

            products_payload = {
                'shop': self.shop_permanent_domain,
                'ids': similar_ids,
                'metafields': metafields,
                'country': country,
                'lang': lang
            }

            products_res = self.session.post(
                'https://platformplugin.biggo.com/api/get_products',
                json=products_payload,
                timeout=self.timeout,
            )
            products_res.raise_for_status()
            data = products_res.json()

            return SearchResponse.from_dict(data)

        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError):
                raise BirseAPIError(f"API error: {e.response.text}")
            else:
                raise BirseConnectionError(f"Connection error: {str(e)}")

    def similar_products(
        self,
        product_id: str,
        image_url: Optional[str] = None,
        country: Optional[str] = None,
        lang: Optional[str] = None,
        metafields: Optional[List[Dict[str, str]]] = None,
    ) -> SearchResponse:
        """
        Find similar products to a given product.

        Args:
            product_id: The product ID to find similar products for
            image_url: Optional specific image URL from the product
            country: Optional country code
            lang: Optional language code
            metafields: Optional metafields filters

        Returns:
            SearchResponse with similar products
        """
        params = {
            'shop': self.shop_permanent_domain,
            'shop_id': self.shop_id,
            'product_id': product_id,
        }

        if image_url:
            params['image_url'] = image_url
        if country:
            params['country'] = country
        if lang:
            params['lang'] = lang
        if metafields:
            params['metafields'] = json.dumps(metafields)

        try:
            response = self.session.get(
                'https://platformplugin.biggo.com/api/similar_products',
                params=params,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()

            return SearchResponse.from_dict(data)

        except requests.exceptions.RequestException as e:
            if isinstance(e, requests.exceptions.HTTPError):
                raise BirseAPIError(f"API error: {e.response.text}")
            else:
                raise BirseConnectionError(f"Connection error: {str(e)}")