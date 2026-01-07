import { formatCurrency, formatRate } from '../formatters'

describe('formatters', () => {
  describe('formatCurrency', () => {
    it('should format currency with 2 decimal places', () => {
      expect(formatCurrency(100)).toBe('100,00')
      expect(formatCurrency(100.5)).toBe('100,50')
      expect(formatCurrency(100.99)).toBe('100,99')
    })

    it('should format large numbers with pt-BR locale', () => {
      expect(formatCurrency(1000)).toBe('1.000,00')
      expect(formatCurrency(1000000)).toBe('1.000.000,00')
    })

    it('should format small numbers', () => {
      expect(formatCurrency(0.01)).toBe('0,01')
      expect(formatCurrency(0.1)).toBe('0,10')
    })

    it('should handle zero', () => {
      expect(formatCurrency(0)).toBe('0,00')
    })

    it('should round to 2 decimal places', () => {
      expect(formatCurrency(100.999)).toBe('101,00')
      expect(formatCurrency(100.994)).toBe('100,99')
    })
  })

  describe('formatRate', () => {
    it('should format rate with 4 decimal places', () => {
      expect(formatRate(5.2)).toBe('5,2000')
      expect(formatRate(5.25)).toBe('5,2500')
      expect(formatRate(5.2567)).toBe('5,2567')
    })

    it('should format large rates with pt-BR locale', () => {
      expect(formatRate(150.5)).toBe('150,5000')
      expect(formatRate(1000.1234)).toBe('1.000,1234')
    })

    it('should format small rates', () => {
      expect(formatRate(0.0067)).toBe('0,0067')
      expect(formatRate(0.1)).toBe('0,1000')
    })

    it('should handle zero', () => {
      expect(formatRate(0)).toBe('0,0000')
    })

    it('should round to 4 decimal places', () => {
      expect(formatRate(5.25678)).toBe('5,2568')
      expect(formatRate(5.25674)).toBe('5,2567')
    })
  })
})

