'use client';

import { useCurrencyConverter } from '@/hooks/useCurrencyConverter';
import CurrencyInput from './CurrencyInput';
import CurrencySelect from './CurrencySelect';
import SwapButton from './SwapButton';
import ConvertButton from './ConvertButton';
import ErrorDisplay from './ErrorDisplay';
import ConversionResult from './ConversionResult';

export default function CurrencyConverter() {
  const {
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
  } = useCurrencyConverter();

  return (
    <div className="max-w-3xl mx-auto">
      <div className="rounded p-8 mb-6" style={{ backgroundColor: '#ffffff', border: '1px solid #e4ebf0' }}>
        <div className="grid md:grid-cols-12 gap-4 items-end">
          <CurrencyInput value={amount} onChange={setAmount} label="Amount" />
          <CurrencySelect value={fromCurrency} onChange={setFromCurrency} label="From" />
          <SwapButton onClick={swapCurrencies} />
          <CurrencySelect value={toCurrency} onChange={setToCurrency} label="To" />
        </div>

        <ConvertButton onClick={convert} loading={loading} />
        <ErrorDisplay error={error} />
      </div>

      {result && <ConversionResult result={result} getCurrencyInfo={getCurrencyInfo} />}
    </div>
  );
}
