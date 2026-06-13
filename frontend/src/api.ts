export const API_BASE_URL = import.meta.env.DEV
  ? 'http://localhost:8000/api/v1'
  : '/api/v1';

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

export interface TokenResponse {
  access_token: string;
  token_type: string;
  username: string;
  role: string;
}

export interface UserResponse {
  id: string;
  username: string;
  role: string;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const headers = new Headers(options?.headers);
  
  // Conditionally set Content-Type to application/json
  if (
    !headers.has('Content-Type') && 
    !(options?.body instanceof URLSearchParams) && 
    !(options?.body instanceof FormData)
  ) {
    headers.set('Content-Type', 'application/json');
  }

  // Inject Bearer Token if present in localStorage
  const token = localStorage.getItem('token');
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    // If we receive a 401 Unauthorized, automatically clear token and redirect/handle if needed
    if (response.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      localStorage.removeItem('role');
      window.dispatchEvent(new Event('auth-change'));
    }

    let errorMessage = `HTTP error! Status: ${response.status}`;
    try {
      const errBody = await response.json();
      if (errBody && errBody.detail) {
        if (typeof errBody.detail === 'string') {
          errorMessage = errBody.detail;
        } else if (Array.isArray(errBody.detail)) {
          errorMessage = errBody.detail.map((e: { msg: string }) => e.msg).join(', ');
        }
      }
    } catch {
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
  login: (username: string, password: string): Promise<TokenResponse> => {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    return request<TokenResponse>('/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: params,
    });
  },

  register: (username: string, password: string, role: string): Promise<UserResponse> => {
    return request<UserResponse>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, password, role }),
    });
  },

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
