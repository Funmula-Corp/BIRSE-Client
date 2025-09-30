import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import FormData from 'form-data';
import * as fs from 'fs';

export interface BirseConfig {
  apiKey: string;
  baseUrl?: string;
  timeout?: number;
}

export interface SearchResult {
  id: string;
  score: number;
  metadata?: Record<string, any>;
  imageUrl?: string;
}

export interface SearchResponse {
  success: boolean;
  results: SearchResult[];
  totalCount?: number;
  processingTime?: number;
}

export class BirseClient {
  private client: AxiosInstance;
  private apiKey: string;

  constructor(config: BirseConfig) {
    this.apiKey = config.apiKey;
    
    this.client = axios.create({
      baseURL: config.baseUrl || 'https://birse-image-insight.biggo.com/api',
      timeout: config.timeout || 30000,
      headers: {
        'X-API-Key': config.apiKey,
      },
    });
  }

  async searchByImage(
    imagePath: string | Buffer,
    options?: {
      maxResults?: number;
      minScore?: number;
      metadata?: Record<string, any>;
    }
  ): Promise<SearchResponse> {
    const formData = new FormData();
    
    if (typeof imagePath === 'string') {
      formData.append('image', fs.createReadStream(imagePath));
    } else {
      formData.append('image', imagePath, 'image.jpg');
    }

    if (options?.maxResults) {
      formData.append('maxResults', options.maxResults.toString());
    }

    if (options?.minScore) {
      formData.append('minScore', options.minScore.toString());
    }

    if (options?.metadata) {
      formData.append('metadata', JSON.stringify(options.metadata));
    }

    const response = await this.client.post<SearchResponse>(
      '/search',
      formData,
      {
        headers: formData.getHeaders(),
      }
    );

    return response.data;
  }

  async searchByUrl(
    imageUrl: string,
    options?: {
      maxResults?: number;
      minScore?: number;
      metadata?: Record<string, any>;
    }
  ): Promise<SearchResponse> {
    const params: any = {
      url: imageUrl,
    };

    if (options?.maxResults) {
      params.maxResults = options.maxResults;
    }

    if (options?.minScore) {
      params.minScore = options.minScore;
    }

    if (options?.metadata) {
      params.metadata = options.metadata;
    }

    const response = await this.client.post<SearchResponse>(
      '/search-by-url',
      params
    );

    return response.data;
  }

  async uploadImage(
    imagePath: string | Buffer,
    metadata?: Record<string, any>
  ): Promise<{ success: boolean; id: string }> {
    const formData = new FormData();
    
    if (typeof imagePath === 'string') {
      formData.append('image', fs.createReadStream(imagePath));
    } else {
      formData.append('image', imagePath, 'image.jpg');
    }

    if (metadata) {
      formData.append('metadata', JSON.stringify(metadata));
    }

    const response = await this.client.post<{ success: boolean; id: string }>(
      '/upload',
      formData,
      {
        headers: formData.getHeaders(),
      }
    );

    return response.data;
  }

  async deleteImage(imageId: string): Promise<{ success: boolean }> {
    const response = await this.client.delete<{ success: boolean }>(
      `/images/${imageId}`
    );

    return response.data;
  }

  async getStatus(): Promise<{ status: string; version: string }> {
    const response = await this.client.get<{ status: string; version: string }>(
      '/status'
    );

    return response.data;
  }
}

export default BirseClient;