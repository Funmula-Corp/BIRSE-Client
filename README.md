# BIRSE Visual Search Client SDKs

Official SDKs for [BIRSE Visual Search](https://birse-image-insight.biggo.com/) - AI-powered image search and visual discovery platform for e-commerce.

## Overview

BIRSE Visual Search helps online retailers enhance their shopping experience with powerful image-based search capabilities. This repository contains official SDKs for integrating BIRSE Visual Search into your applications.

## Available SDKs

- **Node.js SDK** - TypeScript/JavaScript SDK for Node.js applications
- **Python SDK** - Python SDK for Python applications

## Features

- 🔍 **Image Search** - Search for similar products using images
- 📤 **Image Upload** - Upload product images for visual search
- 🔄 **Similar Products** - Find similar products based on existing products
- 🛍️ **Shopify Integration** - Built specifically for Shopify stores

## Installation

### Node.js SDK

```bash
cd nodejs-sdk
npm install
```

### Python SDK

```bash
cd python-sdk
pip install -e .
```

## Quick Start

### Node.js

```typescript
const client = new BirseClient({
  shopId: 'YOUR_SHOP_ID',
  shopPermanentDomain: 'your-shop-name.myshopify.com',
});

// Upload image file object
const uploadResult=await client.uploadImage(imageFile);
// Search by image id
const results = await client.searchImage({
  imageId: uploadResult.image_id,
  country: 'US',
  lang:'EN'
});
```

### Python

```python
from birse import BirseClient

client = BirseClient(
    shop_id='YOUR_SHOP_ID',
    shop_permanent_domain='your-shop-name.myshopify.com'
)

# Upload image file object
upload_result = client.upload_image(image_file)

# Search by image id
results = client.search_image(
    image_id=upload_result['image_id'],
    country='US',
    lang='EN'
)

# Find similar products
similar = client.similar_products(
    product_id='gid://shopify/Product/123456',
    country='US',
    lang='EN'
)
```

## API Documentation

For detailed API documentation, see [API.md](./docs/API.md)

## Links

- 🌐 [BIRSE Image Insight Platform](https://birse-image-insight.biggo.com/)
- 💰 [Pricing Plans](https://birse-image-insight.biggo.com/plans)
- 🛍️ [Shopify App Store](https://apps.shopify.com/birse-visual-search?locale=zh-TW)

## Development

### Node.js SDK

```bash
cd nodejs-sdk
npm run build    # Build TypeScript
npm run lint     # Run linter
```

### Python SDK

```bash
cd python-sdk
pytest           # Run tests
black .          # Format code
flake8           # Run linter
```

## License

MIT License - see LICENSE file for details

## Support

For issues and feature requests, please visit: [GitHub Issues](https://github.com/Funmula-Corp/BIRSE-Client/issues)
