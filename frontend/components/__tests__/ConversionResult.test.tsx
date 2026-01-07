import { render, screen } from '@testing-library/react'
import ConversionResult from '../ConversionResult'

const mockGetCurrencyInfo = (code: string) => {
  const currencies: Record<string, { code: string; name: string }> = {
    USD: { code: 'USD', name: 'US Dollar' },
    BRL: { code: 'BRL', name: 'Brazilian Real' },
    EUR: { code: 'EUR', name: 'Euro' },
  }
  return currencies[code] || { code, name: code }
}

describe('ConversionResult', () => {
  const mockResult = {
    amount: 100.0,
    from: 'USD',
    to: 'BRL',
    rate: 5.2,
    converted_amount: 520.0,
  }

  it('should render formatted values', () => {
    render(
      <ConversionResult result={mockResult} getCurrencyInfo={mockGetCurrencyInfo} />
    )

    expect(screen.getByText('100,00')).toBeInTheDocument()
    expect(screen.getByText('520,00')).toBeInTheDocument()
  })

  it('should display currency names', () => {
    render(
      <ConversionResult result={mockResult} getCurrencyInfo={mockGetCurrencyInfo} />
    )

    expect(screen.getByText('US Dollar')).toBeInTheDocument()
    expect(screen.getByText('Brazilian Real')).toBeInTheDocument()
  })

  it('should display exchange rate', () => {
    render(
      <ConversionResult result={mockResult} getCurrencyInfo={mockGetCurrencyInfo} />
    )

    expect(screen.getByText(/Exchange Rate/i)).toBeInTheDocument()
    expect(screen.getByText(/5,2000/)).toBeInTheDocument()
  })

  it('should display correct labels', () => {
    render(
      <ConversionResult result={mockResult} getCurrencyInfo={mockGetCurrencyInfo} />
    )

    expect(screen.getByText('Original Amount')).toBeInTheDocument()
    expect(screen.getByText('Converted Amount')).toBeInTheDocument()
  })

  it('should handle different currencies', () => {
    const eurResult = {
      amount: 50.0,
      from: 'EUR',
      to: 'USD',
      rate: 1.09,
      converted_amount: 54.5,
    }

    render(
      <ConversionResult result={eurResult} getCurrencyInfo={mockGetCurrencyInfo} />
    )

    expect(screen.getByText('50,00')).toBeInTheDocument()
    expect(screen.getByText('54,50')).toBeInTheDocument()
    expect(screen.getByText('Euro')).toBeInTheDocument()
  })
})

