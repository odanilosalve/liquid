import { convertCurrency } from '../api'
import { API_URL } from '@/constants/api'

describe('api', () => {
  beforeEach(() => {
    global.fetch = jest.fn()
  })

  afterEach(() => {
    jest.restoreAllMocks()
  })

  describe('convertCurrency', () => {
    it('should successfully convert currency', async () => {
      const mockResponse = {
        amount: 100.0,
        from: 'USD',
        to: 'BRL',
        rate: 5.2,
        converted_amount: 520.0,
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      const result = await convertCurrency(100, 'USD', 'BRL')

      expect(result).toEqual(mockResponse)
      expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/convert`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          amount: 100,
          from: 'USD',
          to: 'BRL',
        }),
      })
    })

    it('should throw error when response is not ok', async () => {
      const mockError = { error: 'Invalid currency' }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        json: async () => mockError,
      })

      await expect(convertCurrency(100, 'USD', 'INVALID')).rejects.toThrow(
        'Invalid currency'
      )
    })

    it('should throw default error message when error field is missing', async () => {
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        json: async () => ({}),
      })

      await expect(convertCurrency(100, 'USD', 'BRL')).rejects.toThrow(
        'Currency conversion error'
      )
    })

    it('should handle network errors', async () => {
      ;(global.fetch as jest.Mock).mockRejectedValueOnce(
        new Error('Network error')
      )

      await expect(convertCurrency(100, 'USD', 'BRL')).rejects.toThrow(
        'Network error'
      )
    })

    it('should handle invalid JSON response', async () => {
      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => {
          throw new Error('Invalid JSON')
        },
      })

      await expect(convertCurrency(100, 'USD', 'BRL')).rejects.toThrow()
    })

    it('should call API with correct parameters', async () => {
      const mockResponse = {
        amount: 50.0,
        from: 'EUR',
        to: 'JPY',
        rate: 163.04,
        converted_amount: 8152.0,
      }

      ;(global.fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      })

      await convertCurrency(50, 'EUR', 'JPY')

      expect(global.fetch).toHaveBeenCalledWith(`${API_URL}/convert`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          amount: 50,
          from: 'EUR',
          to: 'JPY',
        }),
      })
    })
  })
})

