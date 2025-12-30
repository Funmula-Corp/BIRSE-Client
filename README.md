<h1 align="center">BIRSE Visual Search Client SDKs</h1>

<p align="center">
  <strong>AI-Powered Visual Search Solution for E-commerce</strong>
</p>

<p align="center">
  <a href="https://apps.shopify.com/birse-visual-search">
    <img src="https://img.shields.io/badge/Shopify-Built%20for%20Shopify-7AB55C?style=flat-square&logo=shopify" alt="Built for Shopify">
  </a>
  <a href="https://apps.shopify.com/birse-visual-search">
    <img src="https://img.shields.io/badge/Rating-5.0%20%E2%98%85-gold?style=flat-square" alt="Rating">
  </a>
  <a href="./LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" alt="License">
  </a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#examples">Examples</a> •
  <a href="#pricing">Pricing</a> •
  <a href="#support">Support</a>
</p>

---

## Overview

**BIRSE Visual Search** is an all-in-one search solution for Shopify merchants, combining **visual search**, **keyword prediction**, and **style-based recommendations**. This repository contains official SDKs for integrating BIRSE into your applications.

| SDK | Language | Status |
|-----|----------|--------|
| [Node.js SDK](./nodejs-sdk) | TypeScript/JavaScript | ✅ Ready |
| [Python SDK](./python-sdk) | Python 3.7+ | ✅ Ready |

---

## Features

| Feature | Description |
|---------|-------------|
| **Image Upload Search** | Let customers upload photos to find matching products |
| **Region Detection** | Identify specific items within complex photos |
| **Similar Products** | Recommend exact matches and style-based alternatives |
| **Multi-language Support** | Supports 25+ languages including English, Chinese, Japanese, and more |
| **Shopify Native** | Built specifically for Shopify with seamless integration |

---

## Installation

### Node.js SDK

```bash
# Using npm
npm install @birse/visual-search-sdk

# Using yarn
yarn add @birse/visual-search-sdk

# From source
cd nodejs-sdk && npm install && npm run build
```

### Python SDK

```bash
# Using pip
pip install birse-visual-search

# From source
cd python-sdk && pip install -e .
```

---

## Quick Start

### Step 1: Get Your Credentials

You'll need two credentials from your Shopify store:
- **Shop ID**: Your unique Shopify shop identifier
- **Shop Permanent Domain**: Your `.myshopify.com` domain

### Step 2: Initialize the Client

<table>
<tr>
<th>Node.js</th>
<th>Python</th>
</tr>
<tr>
<td>

```typescript
import BirseClient from '@birse/visual-search-sdk';

const client = new BirseClient({
  shopId: 'YOUR_SHOP_ID',
  shopPermanentDomain: 'your-shop.myshopify.com'
});
```

</td>
<td>

```python
from birse import BirseClient

client = BirseClient(
    shop_id='YOUR_SHOP_ID',
    shop_permanent_domain='your-shop.myshopify.com'
)
```

</td>
</tr>
</table>

### Step 3: Search by Image

<table>
<tr>
<th>Node.js</th>
<th>Python</th>
</tr>
<tr>
<td>

```typescript
// Upload an image
const upload = await client.uploadImage(imageFile);

// Search for similar products
const results = await client.searchImage({
  imageId: upload.image_id,
  country: 'US',
  lang: 'EN'
});

console.log(results.products);
```

</td>
<td>

```python
# Upload an image
upload = client.upload_image(image_file)

# Search for similar products
results = client.search_image(
    image_id=upload['image_id'],
    country='US',
    lang='EN'
)

print(results.products)
```

</td>
</tr>
</table>

---

## Examples

### Example 1: Basic Image Search (Upload Flow)

This is the most common use case - allow users to upload an image and find similar products.

**Node.js:**
```typescript
import BirseClient from '@birse/visual-search-sdk';

const client = new BirseClient({
  shopId: 'my-shop-123',
  shopPermanentDomain: 'my-awesome-store.myshopify.com'
});

async function handleImageSearch(imageFile: File) {
  // Step 1: Upload the image
  const uploadResult = await client.uploadImage(imageFile);
  console.log(`Image uploaded with ID: ${uploadResult.image_id}`);

  // Step 2: Search for similar products
  const searchResults = await client.searchImage({
    imageId: uploadResult.image_id,
    country: 'US',
    lang: 'EN'
  });

  // Step 3: Display results
  if (searchResults.products.length === 0) {
    console.log('No similar products found');
    return [];
  }

  console.log(`Found ${searchResults.products.length} similar products:`);

  searchResults.products.forEach((product, index) => {
    console.log(`
      ${index + 1}. ${product.title}
         Price: ${product.price} ${product.currency}
         Available: ${product.available ? 'Yes' : 'No'}
         URL: /products/${product.handle}
    `);
  });

  return searchResults.products;
}
```

**Python:**
```python
from birse import BirseClient, BirseAPIError

client = BirseClient(
    shop_id='my-shop-123',
    shop_permanent_domain='my-awesome-store.myshopify.com'
)

def handle_image_search(image_file):
    try:
        # Step 1: Upload the image
        upload_result = client.upload_image(image_file)
        print(f"Image uploaded with ID: {upload_result['image_id']}")

        # Step 2: Search for similar products
        search_results = client.search_image(
            image_id=upload_result['image_id'],
            country='US',
            lang='EN'
        )

        # Step 3: Display results
        if not search_results.products:
            print('No similar products found')
            return []

        print(f"Found {len(search_results.products)} similar products:")

        for i, product in enumerate(search_results.products, 1):
            print(f"""
            {i}. {product.title}
               Price: {product.price} {product.currency}
               Available: {'Yes' if product.available else 'No'}
               URL: /products/{product.handle}
            """)

        return search_results.products

    except BirseAPIError as e:
        print(f"Search failed: {e}")
        return []
```

---

### Example 2: Region-Based Search (Crop Area)

Search within a specific region of an image - useful when the image contains multiple items.

**Node.js:**
```typescript
// Search within a specific region of the image
// xywh = [x, y, width, height] in pixels
const results = await client.searchImage({
  imageId: uploadResult.image_id,
  xywh: [100, 50, 300, 400],  // Focus on this region
  country: 'US',
  lang: 'EN'
});
```

**Python:**
```python
# Search within a specific region of the image
# xywh = (x, y, width, height) in pixels
results = client.search_image(
    image_id=upload_result['image_id'],
    xywh=(100, 50, 300, 400),  # Focus on this region
    country='US',
    lang='EN'
)
```

---

### Example 3: Similar Products Recommendation

Show "You might also like" products based on the currently viewed product.

**Node.js:**
```typescript
async function getRecommendations(currentProductId: string) {
  const similar = await client.similarProducts({
    productId: currentProductId,  // e.g., 'gid://shopify/Product/123456'
    country: 'US',
    lang: 'EN'
  });

  return similar.products.slice(0, 4);  // Return top 4 recommendations
}

// Usage
const recommendations = await getRecommendations('gid://shopify/Product/7654321');
```

**Python:**
```python
def get_recommendations(current_product_id: str):
    similar = client.similar_products(
        product_id=current_product_id,  # e.g., 'gid://shopify/Product/123456'
        country='US',
        lang='EN'
    )

    return similar.products[:4]  # Return top 4 recommendations

# Usage
recommendations = get_recommendations('gid://shopify/Product/7654321')
```

---

### Example 4: With Metafields Filter

Filter search results by custom metafields (e.g., color, material, brand).

**Node.js:**
```typescript
const results = await client.searchImage({
  imageId: uploadResult.image_id,
  country: 'US',
  lang: 'EN',
  metafields: [
    { namespace: 'custom', key: 'color' },
    { namespace: 'custom', key: 'material' }
  ]
});

// Access metafield data from results
results.products.forEach(product => {
  const colorField = product.metafields.find(
    m => m?.reference?.fields?.some(f => f.key === 'color')
  );
  console.log(`${product.title} - Color: ${colorField?.reference?.fields?.[0]?.value}`);
});
```

**Python:**
```python
results = client.search_image(
    image_id=upload_result['image_id'],
    country='US',
    lang='EN',
    metafields=[
        {'namespace': 'custom', 'key': 'color'},
        {'namespace': 'custom', 'key': 'material'}
    ]
)

# Access metafield data from results
for product in results.products:
    print(f"{product.title}")
    for mf in product.metafields:
        if mf and mf.reference:
            for field in mf.reference.fields:
                print(f"  {field.key}: {field.value}")
```

---

### Example 5: Error Handling

**Node.js:**
```typescript
import BirseClient from '@birse/visual-search-sdk';

const client = new BirseClient({
  shopId: 'my-shop-123',
  shopPermanentDomain: 'my-store.myshopify.com'
});

async function safeSearch(imageFile: File) {
  try {
    const upload = await client.uploadImage(imageFile);
    const results = await client.searchImage({
      imageId: upload.image_id
    });
    return { success: true, data: results };
  } catch (error) {
    console.error('Search failed:', error.message);
    return { success: false, error: error.message };
  }
}
```

**Python:**
```python
from birse import BirseClient, BirseAPIError, BirseConnectionError

client = BirseClient(
    shop_id='my-shop-123',
    shop_permanent_domain='my-store.myshopify.com'
)

def safe_search(image_file):
    try:
        upload = client.upload_image(image_file)
        results = client.search_image(image_id=upload['image_id'])
        return {'success': True, 'data': results}
    except BirseAPIError as e:
        print(f"API Error: {e}")
        return {'success': False, 'error': str(e)}
    except BirseConnectionError as e:
        print(f"Connection Error: {e}")
        return {'success': False, 'error': 'Network unavailable'}
```

---

### Example 6: React Integration

```tsx
import { useState } from 'react';
import BirseClient from '@birse/visual-search-sdk';

const client = new BirseClient({
  shopId: process.env.NEXT_PUBLIC_SHOP_ID!,
  shopPermanentDomain: process.env.NEXT_PUBLIC_SHOP_DOMAIN!
});

function VisualSearchWidget() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    try {
      const upload = await client.uploadImage(file);
      const search = await client.searchImage({
        imageId: upload.image_id,
        country: 'US',
        lang: 'EN'
      });
      setResults(search.products);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {loading && <p>Searching...</p>}
      <div className="grid grid-cols-4 gap-4">
        {results.map(product => (
          <div key={product.id}>
            <img src={product.images[0]?.url} alt={product.title} />
            <h3>{product.title}</h3>
            <p>{product.price} {product.currency}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## API Reference

### Methods Overview

| Method | Description | Parameters |
|--------|-------------|------------|
| `uploadImage()` | Upload an image for search | `imageFile: File` |
| `searchImage()` | Search by uploaded image | `imageId`, `xywh?`, `metafields?`, `country?`, `lang?` |
| `similarProducts()` | Find similar products | `productId`, `imageUrl?`, `metafields?`, `country?`, `lang?` |

### Response Structure

```typescript
interface SearchResponse {
  result: boolean;
  products: SearchResult[];
}

interface SearchResult {
  id: string;                    // Shopify product ID
  available: boolean;            // Stock availability
  title: string;                 // Product title
  handle: string;                // URL handle
  images: { url: string }[];     // Product images
  price: string;                 // Product price
  currency: string;              // Currency code
  variants: { nodes: Variant[] };
  collection: Collection[];
  metafields: Metafield[];
}
```

> For complete API documentation, see [docs/API.md](./docs/API.md)

---

## Pricing

BIRSE offers flexible pricing plans for stores of all sizes:

| Plan | Price | Products | Features |
|------|-------|----------|----------|
| **Free** | $0/month | Up to 100 | Basic visual search |
| **Lite** | $5/month | Up to 1,000 | + Priority support |
| **Basic** | $20/month | Up to 3,000 | + Priority support |
| **Recommended** | $50/month | Up to 8,000 | + Priority support |

> All paid plans include a **30-day free trial**

[View Full Pricing Details](https://birse-image-insight.biggo.com/plans) | [Install on Shopify](https://apps.shopify.com/birse-visual-search)

---

## Language Support

BIRSE supports **25+ languages** including:

| | | | |
|---|---|---|---|
| English | Chinese (Traditional) | Chinese (Simplified) | Japanese |
| Korean | Spanish | Portuguese | German |
| French | Italian | Dutch | Russian |
| Arabic | Thai | Vietnamese | Indonesian |

---

## Development

### Node.js SDK

```bash
cd nodejs-sdk
npm install         # Install dependencies
npm run build       # Build TypeScript
npm run lint        # Run linter
npm test            # Run tests
```

### Python SDK

```bash
cd python-sdk
pip install -e ".[dev]"   # Install with dev dependencies
pytest                     # Run tests
black .                    # Format code
flake8                     # Run linter
```

---

## Links

| Resource | Link |
|----------|------|
| BIRSE Platform | [birse-image-insight.biggo.com](https://birse-image-insight.biggo.com/) |
| Shopify App | [apps.shopify.com/birse-visual-search](https://apps.shopify.com/birse-visual-search) |
| Pricing Plans | [birse-image-insight.biggo.com/plans](https://birse-image-insight.biggo.com/plans) |
| API Documentation | [docs/API.md](./docs/API.md) |
| GitHub Issues | [Report an Issue](https://github.com/Funmula-Corp/BIRSE-Client/issues) |

---

## License

MIT License - see [LICENSE](./LICENSE) file for details.

