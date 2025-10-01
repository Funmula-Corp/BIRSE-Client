from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class SelectedOption:
    name: str
    value: str


@dataclass
class Price:
    amount: str
    currency_code: str


@dataclass
class Variant:
    id: str
    available_for_sale: bool
    price: Price
    compare_at_price: Optional[Price]
    selected_options: List[SelectedOption]


@dataclass
class CollectionNode:
    image: Optional[Dict[str, str]]
    title: str
    handle: str


@dataclass
class Collection:
    node: CollectionNode


@dataclass
class MetafieldReference:
    id: str
    type: str
    fields: List[Dict[str, str]]


@dataclass
class Metafield:
    reference: MetafieldReference


@dataclass
class SearchResult:
    id: str
    available: bool
    title: str
    handle: str
    images: List[Optional[Dict[str, str]]]
    price: str
    currency: str
    variants: Dict[str, List[Variant]]
    collection: List[Collection]
    metafields: List[Optional[Metafield]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResult":
        variants_data = data.get("variants", {}).get("nodes", [])
        variants = []
        for v in variants_data:
            price = Price(
                amount=v["price"]["amount"],
                currency_code=v["price"]["currencyCode"]
            )
            compare_at_price = None
            if v.get("compareAtPrice"):
                compare_at_price = Price(
                    amount=v["compareAtPrice"]["amount"],
                    currency_code=v["compareAtPrice"]["currencyCode"]
                )
            selected_options = [
                SelectedOption(name=opt["name"], value=opt["value"])
                for opt in v.get("selectedOptions", [])
            ]
            variants.append(Variant(
                id=v["id"],
                available_for_sale=v["availableForSale"],
                price=price,
                compare_at_price=compare_at_price,
                selected_options=selected_options
            ))

        collections = []
        for c in data.get("collection", []):
            collections.append(Collection(
                node=CollectionNode(
                    image=c["node"].get("image"),
                    title=c["node"]["title"],
                    handle=c["node"]["handle"]
                )
            ))

        metafields = []
        for m in data.get("metafields", []):
            if m:
                metafields.append(Metafield(
                    reference=MetafieldReference(
                        id=m["reference"]["id"],
                        type=m["reference"]["type"],
                        fields=m["reference"]["fields"]
                    )
                ))
            else:
                metafields.append(None)

        return cls(
            id=data["id"],
            available=data["available"],
            title=data["title"],
            handle=data["handle"],
            images=data.get("images", []),
            price=data["price"],
            currency=data["currency"],
            variants={"nodes": variants},
            collection=collections,
            metafields=metafields
        )


@dataclass
class SearchResponse:
    result: bool
    products: List[SearchResult]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SearchResponse":
        products = [SearchResult.from_dict(p) for p in data.get("products", [])]
        return cls(
            result=data["result"],
            products=products
        )