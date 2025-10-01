export interface BirseConfig {
  timeout?: number;
  shopId: string;
  shopPermanentDomain: string;
}

export interface SearchResult {
  id: string;
  available: boolean;
  title: string;
  handle: string;
  images: ({ url: string } | null)[];
  price: string;
  currency: string;
  variants: {
    nodes: [
      {
        id: string;
        availableForSale: boolean;
        price: {
          amount: string;
          currencyCode: string;
        };
        compareAtPrice: null | {
          amount: string;
          currencyCode: string;
        };
        selectedOptions: [
          {
            name: string;
            value: string;
          }
        ];
      }
    ]
  },
  collection: [
    {
      node: {
        image: { url: string } | null;
        title: string;
        handle: string;
      }
    }
  ],
  metafields: ({
    reference: {
      id: string;
      type: string;
      fields: {
        key: string;
        value: string;
      }[]
    }
  } | null)[]
}

export interface SearchResponse {
  result: boolean;
  products: SearchResult[];
}

export interface SearchParams {
  imageId: string;
  xywh?: [number, number, number, number];
  metafields?: { namespace: string, key: string }[];
  country?: string;
  lang?: string;
}

export interface SimilarProductParams {
  productId: string;
  imageUrl?: string;
  country?: string;
  lang?: string;
  metafields?: { namespace: string, key: string }[];
}

export class BirseClient {
  private shopId: string;
  private shopPermanentDomain: string;

  constructor(config: BirseConfig) {
    this.shopId = config.shopId;
    this.shopPermanentDomain = config.shopPermanentDomain;
  }

  async uploadImage(
    imageFile: File
  ): Promise<{ result: boolean; image_id: string }> {
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('shop', this.shopId);

    const response = await fetch('https://api.biggo.com/api/v1/shopify/upload_image', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) throw new Error('Upload failed')
    const data = await response.json() as { result: boolean; image_id: string }
    if (typeof data === 'object' && data.result === false) throw new Error('Upload failed')
    if (!data.image_id) throw new Error('No image id')

    return data;
  }

  async searchImage({
    imageId,
    xywh,
    metafields,
    country,
    lang
  }: SearchParams): Promise<SearchResponse> {

    const similarIdsRes = await fetch('https://api.biggo.com/api/v1/shopify/similar_image', {
      method: 'POST',
      body: JSON.stringify({
        image_id: imageId,
        xywh: xywh,
        is_orientation: false,
        shop: this.shopId
      })
    })
    const similarIds = await similarIdsRes.json() as string[]
    if (!similarIdsRes.ok) throw new Error((similarIds as any)?.error?.message || 'Search failed')
    if (!Array.isArray(similarIds) || similarIds.length === 0) {
      return { result: true, products: [] }
    }
    const getProductRes = await fetch('https://platformplugin.biggo.com/api/get_products', {
      method: 'POST',
      body: JSON.stringify({
        shop: this.shopPermanentDomain,
        ids: similarIds,
        metafields: metafields,
        country: country,
        lang: lang
      })
    })
    const data = await getProductRes.json() as SearchResponse
    if (!getProductRes.ok) throw new Error((data as any)?.error?.message || 'Get products failed')

    return data;
  }


  async similarProducts({
    productId,
    imageUrl,
    country,
    lang,
    metafields
  }: SimilarProductParams): Promise<SearchResponse> {
    const searchParams = new URLSearchParams()
    searchParams.append('shop', this.shopPermanentDomain)
    searchParams.append('shop_id', this.shopId)
    searchParams.append('product_id', productId)
    if (imageUrl) searchParams.append('image_url', imageUrl)
    if (country) searchParams.append('country', country)
    if (lang) searchParams.append('lang', lang)
    if (metafields) {
      searchParams.append('metafields', JSON.stringify(metafields))
    }
    const response = await fetch(`https://platformplugin.biggo.com/api/similar_products?${searchParams.toString()}`)
    const data = await response.json() as SearchResponse
    return data;
  }
}

export default BirseClient;