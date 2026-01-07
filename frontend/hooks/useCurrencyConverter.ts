import { useState } from 'react';
import { convertCurrency } from '@/services/api';
import { ConversionResult } from '@/types/conversion';
import { CURRENCIES } from '@/constants/currencies';

export function useCurrencyConverter() {
  const [amount, setAmount] = useState<string>('100');
  const [fromCurrency, setFromCurrency] = useState<string>('USD');
  const [toCurrency, setToCurrency] = useState<string>('BRL');
  const [result, setResult] = useState<ConversionResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const convert = async () => {
    if (!amount || parseFloat(amount) <= 0) {
      setError('Please enter a valid amount');
      return;
    }

    if (fromCurrency === toCurrency) {
      setError('Please select different currencies');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await convertCurrency(parseFloat(amount), fromCurrency, toCurrency);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Currency conversion error');
    } finally {
      setLoading(false);
    }
  };

  const swapCurrencies = () => {
    setFromCurrency(toCurrency);
    setToCurrency(fromCurrency);
    if (result) {
      setResult(null);
    }
  };

  const getCurrencyInfo = (code: string) => {
    return CURRENCIES.find(c => c.code === code) || { code, name: code };
  };

  return {
    amount,
    fromCurrency,
    toCurrency,
    result,
    loading,
    error,
    setAmount,
    setFromCurrency,
    setToCurrency,
    convert,
    swapCurrencies,
    getCurrencyInfo,
  };
}


