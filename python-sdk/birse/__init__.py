from .client import BirseClient
from .exceptions import BirseException, BirseAPIError, BirseConnectionError
from .models import (
    SearchResult,
    SearchResponse,
    SelectedOption,
    Price,
    Variant,
    CollectionNode,
    Collection,
    MetafieldReference,
    Metafield,
)

__version__ = "1.0.0"
__all__ = [
    "BirseClient",
    "BirseException",
    "BirseAPIError",
    "BirseConnectionError",
    "SearchResult",
    "SearchResponse",
    "SelectedOption",
    "Price",
    "Variant",
    "CollectionNode",
    "Collection",
    "MetafieldReference",
    "Metafield",
]