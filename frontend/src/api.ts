export const API_BASE_URL = 'http://localhost:8000/api/v1';

export type TicketSource = 'email' | 'chat' | 'web' | 'phone';
export type TicketStatus = 'open' | 'in_progress' | 'resolved' | 'closed';
export type TicketCategory = 'billing' | 'technical_issue' | 'account_access' | 'refund' | 'general_query';
export type TicketSentiment = 'positive' | 'neutral' | 'negative';
export type TicketPriority = 'low' | 'medium' | 'high' | 'urgent';

export interface PredictionRead {
  id: string;
  category: string;
  category_confidence: number;
  sentiment: string;
  sentiment_confidence: number;
  priority: string;
  priority_confidence: number;
  model_version: string | null;
  created_at: string;
}

export interface TicketRead {
  id: string;
  customer_id: string | null;
  subject: string;
  description: string;
  source: TicketSource;
  status: TicketStatus;
  prediction: PredictionRead | null;
  created_at: string;
  updated_at: string;
}

export interface TicketCreate {
  customer_id?: string;
  subject: string;
  description: string;
  source: TicketSource;
}

export interface TicketListResponse {
  items: TicketRead[];
  limit: number;
  offset: number;
  total: number;
}

export interface HealthResponse {
  status: string;
  service: string;
}

export interface ReloadModelResponse {
  status: string;
  model_version: string | null;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {}),
    },
  });

  if (!response.ok) {
    let errorMessage = `HTTP error! Status: ${response.status}`;
    try {
      const errBody = await response.json();
      if (errBody && errBody.detail) {
        if (typeof errBody.detail === 'string') {
          errorMessage = errBody.detail;
        } else if (Array.isArray(errBody.detail)) {
          errorMessage = errBody.detail.map((e: any) => e.msg).join(', ');
        }
      }
    } catch (_) {
      // fallback to status text
    }
    throw new Error(errorMessage);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

export const api = {
  getHealth: (): Promise<HealthResponse> => {
    return request<HealthResponse>('/health');
  },

  getTickets: (params?: {
    limit?: number;
    offset?: number;
    status?: TicketStatus;
    priority?: TicketPriority;
    category?: TicketCategory;
    sentiment?: TicketSentiment;
  }): Promise<TicketListResponse> => {
    const query = new URLSearchParams();
    if (params) {
      if (params.limit !== undefined) query.append('limit', params.limit.toString());
      if (params.offset !== undefined) query.append('offset', params.offset.toString());
      if (params.status) query.append('status', params.status);
      if (params.priority) query.append('priority', params.priority);
      if (params.category) query.append('category', params.category);
      if (params.sentiment) query.append('sentiment', params.sentiment);
    }
    const queryString = query.toString() ? `?${query.toString()}` : '';
    return request<TicketListResponse>(`/tickets${queryString}`);
  },

  getTicket: (id: string): Promise<TicketRead> => {
    return request<TicketRead>(`/tickets/${id}`);
  },

  createTicket: (ticket: TicketCreate): Promise<TicketRead> => {
    return request<TicketRead>('/tickets', {
      method: 'POST',
      body: JSON.stringify(ticket),
    });
  },

  updateTicketStatus: (id: string, status: TicketStatus): Promise<TicketRead> => {
    return request<TicketRead>(`/tickets/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    });
  },

  rerunPrediction: (id: string): Promise<TicketRead> => {
    return request<TicketRead>(`/tickets/${id}/predict`, {
      method: 'POST',
    });
  },

  deleteTicket: (id: string): Promise<void> => {
    return request<void>(`/tickets/${id}`, {
      method: 'DELETE',
    });
  },

  reloadModels: (): Promise<ReloadModelResponse> => {
    return request<ReloadModelResponse>('/model/reload', {
      method: 'POST',
    });
  },
};
