# BIRSE API Documentation

This document describes the API endpoints used by the BIRSE Client SDK for visual search functionality.

## Configuration

All requests require `shopId` or `shopPermanentDomain` parameter that identifies your Shopify store.

`shopId` is a string of numbers, can be obtained by entering the following javascript in your Shopify store page devtool console:
```javascript
JSON.parse(document.getElementById('shopify-features').textContent).shopId
```

`shopPermanentDomain` is your shop's permanent domain, usually in the format `your-shop-name.myshopify.com`,
you can find it by entering the following javascript in your Shopify store page devtool console:
```javascript
Shopify.shop
```


## Endpoints

### 1. Upload Image

Upload an image for visual search processing.

**URL**: `POST https://api.biggo.com/api/v1/shopify/upload_image`

**Content-Type**: `multipart/form-data`

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | File | Yes | The image file to upload. Supported formats: JPEG (.jpg), PNG (.png), WebP (.webp) |
| `shop` | string | Yes | Your shop ID |

**Response**:
```json
{
  "result": true,
  "image_id": "string"
}
```

**Example Request**:
```javascript
const formData = new FormData();
formData.append('image', imageFile);
formData.append('shop', 'your-shop-id');

const response = await fetch('https://api.biggo.com/api/v1/shopify/upload_image', {
  method: 'POST',
  body: formData
});
```

### 2. Find Similar Images

Find similar products based on an uploaded image.

**URL**: `POST https://api.biggo.com/api/v1/shopify/similar_image`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "image_id": "string",
  "xywh": [number, number, number, number],
  "shop": "string"
}
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `shop` | string | Yes | Your shop ID |
| `image_id` | string | Yes | The ID returned from the upload image endpoint |
| `xywh` | number[] | No | Bounding box coordinates [x, y, width, height] for cropping |
| `is_orientation` | boolean | No | Whether to consider image orientation|

**Response**:
```json
["gid://shopify/Product/123456789", "gid://shopify/Product/987654321"]
```

**Example Request**:
```javascript
const response = await fetch('https://api.biggo.com/api/v1/shopify/similar_image', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    image_id: 'uploaded_image_id',
    xywh: [0, 0, 100, 100],
    is_orientation: false,
    shop: 'your-shop-id'
  })
});
```

### 3. Get Products

Retrieve detailed product information by product IDs.

**URL**: `POST https://platformplugin.biggo.com/api/get_products`

**Content-Type**: `application/json`

**Request Body**:
```json
{
  "shop": "string",
  "ids": "string"[],
  "metafields": {"namespace": "string", "key": "string"}[],
  "country": "string",
  "lang": "string"
}
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `shop` | string | Yes | Your permanent shop domain (e.g., "shop-name.myshopify.com") |
| `ids` | string[] | Yes | Array of product IDs to retrieve |
| `metafields` | object[] | No | Product metafields to include in the response |
| `country` | string | No | Country code for localization (see [Shopify CountryCode](https://shopify.dev/docs/api/storefront/latest/enums/countrycode)) |
| `lang` | string | No | Language code for localization (see [Shopify LanguageCode](https://shopify.dev/docs/api/storefront/latest/enums/LanguageCode)) |

**Response**:
```json
{
  "result": true,
  "products": [
    {
      "id": "string",
      "available": true,
      "title": "string",
      "handle": "string",
      "images": [{"url": "string"}],
      "price": "string",
      "currency": "string",
      "variants": {
        "nodes": [
          {
            "id": "string",
            "availableForSale": true,
            "price": {
              "amount": "string",
              "currencyCode": "string"
            },
            "compareAtPrice": {
              "amount": "string",
              "currencyCode": "string"
            },
            "selectedOptions": [
              {
                "name": "string",
                "value": "string"
              }
            ]
          }
        ]
      },
      "collection": [
        {
          "node": {
            "image": {"url": "string"},
            "title": "string",
            "handle": "string"
          }
        }
      ],
      "metafields": [
        {
          "reference": {
            "id": "string",
            "type": "string",
            "fields": [
              {
                "key": "string",
                "value": "string"
              }
            ]
          }
        }
      ]
    }
  ]
}
```

**Example Request**:
```javascript
const response = await fetch('https://platformplugin.biggo.com/api/get_products', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    shop: 'shop-name.myshopify.com',
    ids: ['gid://shopify/Product/123456789', 'gid://shopify/Product/987654321'],
    metafields: [
      {
        "namespace": "custom",
        "key": "metadata-key"
      }
    ],
    country: 'US',
    lang: 'EN'
  })
});
```

### 4. Similar Products

Find similar products based on an existing product.

**URL**: `GET https://platformplugin.biggo.com/api/similar_products`

**Query Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `shop` | string | Yes | Your permanent shop domain |
| `shop_id` | string | Yes | Your shop ID |
| `product_id` | string | Yes | The product ID to find similar products for |
| `image_url` | string | No | Specific image URL to use for comparison |
| `country` | string | No | Country code for localization (see [Shopify CountryCode](https://shopify.dev/docs/api/storefront/latest/enums/countrycode)) |
| `lang` | string | No | Language code for localization (see [Shopify LanguageCode](https://shopify.dev/docs/api/storefront/latest/enums/LanguageCode)) |
| `metafields` | string | No | JSON stringified array of metafields to include |

**Response**:
Same as Get Products endpoint response format.

**Example Request**:
```javascript
const searchParams = new URLSearchParams();
searchParams.append('shop', 'shop-name.myshopify.com');
searchParams.append('shop_id', 'your-shop-id');
searchParams.append('product_id', '123456789');
searchParams.append('image_url', 'https://example.com/image.jpg');
searchParams.append('country', 'US');
searchParams.append('lang', 'EN');
searchParams.append('metafields', JSON.stringify([
  {"namespace": "custom", "key": "metadata-key"}
]));

const response = await fetch(`https://platformplugin.biggo.com/api/similar_products?${searchParams.toString()}`);
```

## Usage Flow

1. **Upload Image**: Upload an image using the `/upload_image` endpoint
2. **Find Similar**: Use the returned `image_id` to find similar products via `/similar_image`
3. **Get Products**: Retrieve detailed product information using the product IDs from step 2
4. **Similar Products**: Alternatively, find similar products based on an existing product ID
