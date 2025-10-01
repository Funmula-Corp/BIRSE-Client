# BIRSE Visual Search Client SDKs

Official SDKs for [BIRSE Visual Search](https://birse-image-insight.biggo.com/) - AI-powered image search and visual discovery platform for e-commerce.

## Overview

BIRSE Visual Search helps online retailers enhance their shopping experience with powerful image-based search capabilities. This repository contains official SDKs for integrating BIRSE Visual Search into your applications.

## Available SDKs

- **Node.js SDK** - TypeScript/JavaScript SDK for Node.js applications
- **Python SDK** - Python SDK for Python applications

## Features

- 🔍 **Image Search** - Search for similar products using images

## Installation

### Node.js SDK

```bash
cd nodejs-sdk
npm install
```

### Python SDK

```bash
cd python-sdk
pip install -r requirements.txt
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

client = BirseClient(api_key='YOUR_API_KEY')

# Search by image file
results = client.search_by_image('product.jpg', 
                                  max_results=10,
                                  min_score=0.8)
```

## API Documentation

For detailed API documentation, visit:

- [API Documentation](API.md) this file contains detailed information about each endpoint, parameters, and response formats.
- [BIRSE Image Insight Platform](https://birse-image-insight.biggo.com/)
- [Shopify App Store](https://apps.shopify.com/birse-visual-search?locale=zh-TW)

## Development

### Node.js SDK

```bash
cd nodejs-sdk
npm install
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
