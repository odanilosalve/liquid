import { API_URL } from '@/constants/api';
import { ConversionResult } from '@/types/conversion';

function getAuthToken(): string | null {
  if (typeof window === 'undefined') {
    return null;
  }
  return localStorage.getItem('liquid_auth_token');
}

export async function convertCurrency(
  amount: number,
  from: string,
  to: string
): Promise<ConversionResult> {
  const token = getAuthToken();
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}/convert`, {
    method: 'POST',
    headers,
    body: JSON.stringify({
      amount,
      from,
      to,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    if (response.status === 401) {
      if (typeof window !== 'undefined') {
        localStorage.removeItem('liquid_auth_token');
        localStorage.removeItem('liquid_auth_user');
      }
      throw new Error('Session expired. Please log in again.');
    }
    throw new Error(data.error || 'Currency conversion error');
  }

  return data;
}


