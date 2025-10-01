# BIRSE Visual Search API Documentation

Official API documentation for BIRSE Visual Search Client SDKs for Shopify.

## Overview

BIRSE provides AI-powered visual search capabilities for Shopify stores, enabling customers to search for products using images.

## Authentication

Both SDKs require your Shopify store credentials:
- **Shop ID**: Your unique Shopify shop identifier
- **Shop Permanent Domain**: Your shop's permanent domain (e.g., `your-shop.myshopify.com`)

## Client Initialization

### Node.js

```typescript
import BirseClient from '@birse/visual-search-sdk';

const client = new BirseClient({
  shopId: 'YOUR_SHOP_ID',
  shopPermanentDomain: 'your-shop-name.myshopify.com',
  timeout: 30000  // optional, in milliseconds
});
```

### Python

```python
from birse import BirseClient

client = BirseClient(
    shop_id='YOUR_SHOP_ID',
    shop_permanent_domain='your-shop-name.myshopify.com',
    timeout=30  # optional, in seconds
)
```

---

## API Methods

### 1. Upload Image

Upload a product image for visual search.

**Node.js:**

```typescript
const result = await client.uploadImage(imageFile);
// Returns: { result: boolean, image_id: string }
```

**Python:**

```python
result = client.upload_image(image_file)
# Returns: { 'result': bool, 'image_id': str }
```

**Parameters:**
- `imageFile` / `image_file`: File object from file input

**Returns:**
```json
{
  "result": true,
  "image_id": "abc123..."
}
```

**Endpoint:** `POST https://api.biggo.com/api/v1/shopify/upload_image`

---

### 2. Search Image

Search for similar products using an uploaded image ID.

**Node.js:**

```typescript
const results = await client.searchImage({
  imageId: 'abc123...',
  xywh: [100, 100, 500, 500],  // optional crop coordinates
  metafields: [{ namespace: 'custom', key: 'color' }],  // optional
  country: 'US',  // optional
  lang: 'EN'  // optional
});
```

**Python:**

```python
results = client.search_image(
    image_id='abc123...',
    xywh=(100, 100, 500, 500),  # optional crop coordinates
    metafields=[{'namespace': 'custom', 'key': 'color'}],  # optional
    country='US',  # optional
    lang='EN'  # optional
)
```

**Parameters:**
- `imageId` / `image_id`: Image ID from upload
- `xywh`: Optional crop coordinates `[x, y, width, height]`
- `metafields`: Optional array of metafield filters
- `country`: Optional country code
- `lang`: Optional language code

**Returns:**

```typescript
{
  result: boolean;
  products: SearchResult[];
}
```

**SearchResult Structure:**

```typescript
{
  id: string;
  available: boolean;
  title: string;
  handle: string;
  images: ({ url: string } | null)[];
  price: string;
  currency: string;
  variants: {
    nodes: [{
      id: string;
      availableForSale: boolean;
      price: {
        amount: string;
        currencyCode: string;
      };
      compareAtPrice: {
        amount: string;
        currencyCode: string;
      } | null;
      selectedOptions: [{
        name: string;
        value: string;
      }];
    }]
  };
  collection: [{
    node: {
      image: { url: string } | null;
      title: string;
      handle: string;
    }
  }];
  metafields: ({
    reference: {
      id: string;
      type: string;
      fields: {
        key: string;
        value: string;
      }[]
    }
  } | null)[];
}
```

**Endpoints:**
1. `POST https://api.biggo.com/api/v1/shopify/similar_image`
2. `POST https://platformplugin.biggo.com/api/get_products`

---

### 3. Similar Products

Find products similar to an existing product.

**Node.js:**

```typescript
const results = await client.similarProducts({
  productId: 'gid://shopify/Product/123456',
  imageUrl: 'https://...jpg',  // optional
  country: 'US',  // optional
  lang: 'EN',  // optional
  metafields: [{ namespace: 'custom', key: 'color' }]  // optional
});
```

**Python:**

```python
results = client.similar_products(
    product_id='gid://shopify/Product/123456',
    image_url='https://...jpg',  # optional
    country='US',  # optional
    lang='EN',  # optional
    metafields=[{'namespace': 'custom', 'key': 'color'}]  # optional
)
```

**Parameters:**
- `productId` / `product_id`: Shopify product ID (GID format)
- `imageUrl` / `image_url`: Optional specific image URL from product
- `country`: Optional country code
- `lang`: Optional language code
- `metafields`: Optional metafield filters

**Returns:** Same structure as `searchImage` (SearchResponse)

**Endpoint:** `GET https://platformplugin.biggo.com/api/similar_products`

---

## Data Models

### Python

```python
from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class SearchResponse:
    result: bool
    products: List[SearchResult]

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
```

### TypeScript

```typescript
export interface SearchResponse {
  result: boolean;
  products: SearchResult[];
}

export interface SearchResult {
  id: string;
  available: boolean;
  title: string;
  handle: string;
  images: ({ url: string } | null)[];
  price: string;
  currency: string;
  variants: { nodes: Variant[] };
  collection: Collection[];
  metafields: (Metafield | null)[];
}
```

---

## Error Handling

### Node.js

```typescript
try {
  const results = await client.searchImage({ imageId: 'abc123' });
} catch (error) {
  console.error('Search failed:', error.message);
}
```

### Python

```python
from birse import BirseAPIError, BirseConnectionError

try:
    results = client.search_image(image_id='abc123')
except BirseAPIError as e:
    print(f'API error: {e}')
except BirseConnectionError as e:
    print(f'Connection error: {e}')
```

**Exception Types (Python):**
- `BirseException`: Base exception
- `BirseAPIError`: API errors (HTTP 4xx/5xx)
- `BirseConnectionError`: Network connection errors

---

## Complete Example

### Node.js

```typescript
import BirseClient from '@birse/visual-search-sdk';

const client = new BirseClient({
  shopId: 'YOUR_SHOP_ID',
  shopPermanentDomain: 'your-shop.myshopify.com'
});

async function searchProducts(imageFile: File) {
  try {
    const upload = await client.uploadImage(imageFile);
    console.log('Uploaded:', upload.image_id);

    const results = await client.searchImage({
      imageId: upload.image_id,
      country: 'US',
      lang: 'EN'
    });

    console.log(`Found ${results.products.length} products`);
    results.products.forEach(product => {
      console.log(`- ${product.title}: ${product.price} ${product.currency}`);
    });
  } catch (error) {
    console.error('Error:', error);
  }
}
```

### Python

```python
from birse import BirseClient, BirseAPIError

client = BirseClient(
    shop_id='YOUR_SHOP_ID',
    shop_permanent_domain='your-shop.myshopify.com'
)

def search_products(image_file):
    try:
        upload = client.upload_image(image_file)
        print(f"Uploaded: {upload['image_id']}")

        results = client.search_image(
            image_id=upload['image_id'],
            country='US',
            lang='EN'
        )

        print(f"Found {len(results.products)} products")
        for product in results.products:
            print(f"- {product.title}: {product.price} {product.currency}")

    except BirseAPIError as e:
        print(f"Error: {e}")
```

---

## Resources

- **Platform**: [BIRSE Image Insight](https://birse-image-insight.biggo.com/)
- **Pricing**: [View Plans](https://birse-image-insight.biggo.com/plans)
- **Shopify App**: [Install on Shopify](https://apps.shopify.com/birse-visual-search?locale=zh-TW)
- **Support**: [GitHub Issues](https://github.com/Funmula-Corp/BIRSE-Client/issues)
