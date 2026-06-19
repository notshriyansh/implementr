export interface PaperAuthor {
  name: string;
}

export interface Paper {
  title: string;
  summary: string;
  pdf_url: string;
  published: string;
  authors: PaperAuthor[];
}

export interface PaperSearchResponse {
  papers: Paper[];
}

export interface IngestionResponse {
  total_chunks: number;

  sample_chunk: {
    chunk_id: string;
    text?: string;
    content?: string;
  };
}
