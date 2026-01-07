import { API_URL } from '@/constants/api';
import { ConversionResult } from '@/types/conversion';

export async function convertCurrency(
  amount: number,
  from: string,
  to: string
): Promise<ConversionResult> {
  const response = await fetch(`${API_URL}/convert`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      amount,
      from,
      to,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.error || 'Erro ao converter moeda');
  }

  return data;
}

