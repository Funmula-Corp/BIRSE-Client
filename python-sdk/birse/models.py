from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class SearchResult:
    """Represents a single search result"""
    
    id: str
    score: float
    metadata: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResult":
        return cls(
            id=data["id"],
            score=data["score"],
            metadata=data.get("metadata"),
            image_url=data.get("imageUrl"),
        )


@dataclass
class SearchResponse:
    """Represents a search response from the API"""
    
    success: bool
    results: List[SearchResult]
    total_count: Optional[int] = None
    processing_time: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResponse":
        results = [SearchResult.from_dict(r) for r in data.get("results", [])]
        return cls(
            success=data["success"],
            results=results,
            total_count=data.get("totalCount"),
            processing_time=data.get("processingTime"),
        )