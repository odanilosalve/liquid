import { renderHook, act, waitFor } from '@testing-library/react'
import '@testing-library/jest-dom'
import { useCurrencyConverter } from '../useCurrencyConverter'
import { convertCurrency } from '@/services/api'

jest.mock('@/services/api')

describe('useCurrencyConverter', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  it('should initialize with default values', () => {
    const { result } = renderHook(() => useCurrencyConverter())

    expect(result.current.amount).toBe('100')
    expect(result.current.fromCurrency).toBe('USD')
    expect(result.current.toCurrency).toBe('BRL')
    expect(result.current.result).toBeNull()
    expect(result.current.loading).toBe(false)
    expect(result.current.error).toBeNull()
  })

  it('should update amount', () => {
    const { result } = renderHook(() => useCurrencyConverter())

    act(() => {
      result.current.setAmount('200')
    })

    expect(result.current.amount).toBe('200')
  })

  it('should update fromCurrency', () => {
    const { result } = renderHook(() => useCurrencyConverter())

    act(() => {
      result.current.setFromCurrency('EUR')
    })

    expect(result.current.fromCurrency).toBe('EUR')
  })

  it('should update toCurrency', () => {
    const { result } = renderHook(() => useCurrencyConverter())

    act(() => {
      result.current.setToCurrency('JPY')
    })

    expect(result.current.toCurrency).toBe('JPY')
  })

  it('should successfully convert currency', async () => {
    const mockResult = {
      amount: 100.0,
      from: 'USD',
      to: 'BRL',
      rate: 5.2,
      converted_amount: 520.0,
    }

    ;(convertCurrency as jest.Mock).mockResolvedValueOnce(mockResult)

    const { result } = renderHook(() => useCurrencyConverter())

    await act(async () => {
      await result.current.convert()
    })

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.result).toEqual(mockResult)
    expect(result.current.error).toBeNull()
    expect(convertCurrency).toHaveBeenCalledWith(100, 'USD', 'BRL')
  })

  it('should handle conversion error', async () => {
    const mockError = new Error('API Error')
    ;(convertCurrency as jest.Mock).mockRejectedValueOnce(mockError)

    const { result } = renderHook(() => useCurrencyConverter())

    await act(async () => {
      await result.current.convert()
    })

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })

    expect(result.current.error).toBe('API Error')
    expect(result.current.result).toBeNull()
  })

  it('should set error for invalid amount', async () => {
    const { result } = renderHook(() => useCurrencyConverter())

    act(() => {
      result.current.setAmount('')
    })

    await act(async () => {
      await result.current.convert()
    })

    expect(result.current.error).toBe('Please enter a valid amount')
    expect(result.current.loading).toBe(false)
    expect(convertCurrency).not.toHaveBeenCalled()
  })

  it('should set error for zero amount', async () => {
    const { result } = renderHook(() => useCurrencyConverter())

    act(() => {
      result.current.setAmount('0')
    })

    await act(async () => {
      await result.current.convert()
    })

    expect(result.current.error).toBe('Please enter a valid amount')
    expect(convertCurrency).not.toHaveBeenCalled()
  })

  it('should set error for same currencies', async () => {
    const { result } = renderHook(() => useCurrencyConverter())

    act(() => {
      result.current.setFromCurrency('USD')
      result.current.setToCurrency('USD')
    })

    await act(async () => {
      await result.current.convert()
    })

    expect(result.current.error).toBe('Please select different currencies')
    expect(convertCurrency).not.toHaveBeenCalled()
  })

  it('should swap currencies', () => {
    const { result } = renderHook(() => useCurrencyConverter())

    act(() => {
      result.current.setFromCurrency('EUR')
      result.current.setToCurrency('GBP')
    })

    act(() => {
      result.current.swapCurrencies()
    })

    expect(result.current.fromCurrency).toBe('GBP')
    expect(result.current.toCurrency).toBe('EUR')
  })

  it('should clear result when swapping currencies', async () => {
    const mockResult = {
      amount: 100.0,
      from: 'USD',
      to: 'BRL',
      rate: 5.2,
      converted_amount: 520.0,
    }

    ;(convertCurrency as jest.Mock).mockResolvedValueOnce(mockResult)

    const { result } = renderHook(() => useCurrencyConverter())

    await act(async () => {
      await result.current.convert()
    })

    await waitFor(() => {
      expect(result.current.result).not.toBeNull()
    })

    act(() => {
      result.current.swapCurrencies()
    })

    expect(result.current.result).toBeNull()
  })

  it('should get currency info', () => {
    const { result } = renderHook(() => useCurrencyConverter())

    const usdInfo = result.current.getCurrencyInfo('USD')
    expect(usdInfo).toEqual({ code: 'USD', name: 'US Dollar' })

    const brlInfo = result.current.getCurrencyInfo('BRL')
    expect(brlInfo).toEqual({ code: 'BRL', name: 'Brazilian Real' })
  })

  it('should return default info for unknown currency', () => {
    const { result } = renderHook(() => useCurrencyConverter())

    const unknownInfo = result.current.getCurrencyInfo('UNKNOWN')
    expect(unknownInfo).toEqual({ code: 'UNKNOWN', name: 'UNKNOWN' })
  })

  it('should set loading state during conversion', async () => {
    let resolvePromise: (value: any) => void
    const promise = new Promise((resolve) => {
      resolvePromise = resolve
    })

    ;(convertCurrency as jest.Mock).mockReturnValueOnce(promise)

    const { result } = renderHook(() => useCurrencyConverter())

    act(() => {
      result.current.convert()
    })

    expect(result.current.loading).toBe(true)

    await act(async () => {
      resolvePromise!({
        amount: 100.0,
        from: 'USD',
        to: 'BRL',
        rate: 5.2,
        converted_amount: 520.0,
      })
      await promise
    })

    await waitFor(() => {
      expect(result.current.loading).toBe(false)
    })
  })

  it('should clear error and result before new conversion', async () => {
    const firstResult = {
      amount: 50.0,
      from: 'EUR',
      to: 'GBP',
      rate: 0.86,
      converted_amount: 43.0,
    }

    const secondResult = {
      amount: 100.0,
      from: 'USD',
      to: 'BRL',
      rate: 5.2,
      converted_amount: 520.0,
    }

    ;(convertCurrency as jest.Mock)
      .mockResolvedValueOnce(firstResult)
      .mockResolvedValueOnce(secondResult)

    const { result } = renderHook(() => useCurrencyConverter())

    await act(async () => {
      await result.current.convert()
    })

    await waitFor(() => {
      expect(result.current.result).toEqual(firstResult)
    })

    await act(async () => {
      await result.current.convert()
    })

    await waitFor(() => {
      expect(result.current.error).toBeNull()
      expect(result.current.result).toEqual(secondResult)
    })
  })
})

