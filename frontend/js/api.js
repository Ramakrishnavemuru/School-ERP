/**
 * Centralized API Client for School/College ERP
 */
const API_BASE = '/api';

const api = {
  getToken() {
    return localStorage.getItem('token');
  },

  getHeaders(isFormData = false) {
    const headers = {};
    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    if (!isFormData) {
      headers['Content-Type'] = 'application/json';
    }
    return headers;
  },

  async request(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint.startsWith('/') ? endpoint : '/' + endpoint}`;
    const isFormData = options.body instanceof FormData;

    const config = {
      method: options.method || 'GET',
      headers: {
        ...this.getHeaders(isFormData),
        ...(options.headers || {})
      },
      ...options
    };

    if (config.body && !isFormData && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body);
    }

    try {
      const response = await fetch(url, config);

      // Handle unauthenticated 401
      if (response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        if (!window.location.pathname.includes('login.html')) {
          window.location.href = '/frontend/login.html?expired=1';
        }
        throw new Error('Session expired. Please log in again.');
      }

      // Handle forbidden 403
      if (response.status === 403) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || 'Access denied. You do not have permission for this action.');
      }

      // Handle 204 No Content
      if (response.status === 204) {
        return null;
      }

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        const errorMsg = data.detail || (typeof data === 'string' ? data : 'An error occurred');
        throw new Error(errorMsg);
      }

      return data;
    } catch (error) {
      console.error(`API Error [${config.method} ${endpoint}]:`, error);
      throw error;
    }
  },

  get(endpoint, params = {}) {
    let query = '';
    const cleanParams = Object.entries(params).filter(([_, v]) => v !== null && v !== undefined && v !== '');
    if (cleanParams.length > 0) {
      const searchParams = new URLSearchParams();
      cleanParams.forEach(([k, v]) => searchParams.append(k, v));
      query = `?${searchParams.toString()}`;
    }
    return this.request(`${endpoint}${query}`, { method: 'GET' });
  },

  post(endpoint, body = {}) {
    return this.request(endpoint, { method: 'POST', body });
  },

  put(endpoint, body = {}) {
    return this.request(endpoint, { method: 'PUT', body });
  },

  patch(endpoint, body = {}) {
    return this.request(endpoint, { method: 'PATCH', body });
  },

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
};

window.api = api;
