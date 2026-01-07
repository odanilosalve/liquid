import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import CurrencySelect from '../CurrencySelect'

describe('CurrencySelect', () => {
  it('should render with label and options', () => {
    const onChange = jest.fn()
    render(<CurrencySelect value="USD" onChange={onChange} label="From" />)

    expect(screen.getByLabelText('From')).toBeInTheDocument()
    expect(screen.getByText('US Dollar')).toBeInTheDocument()
    expect(screen.getByText('Brazilian Real')).toBeInTheDocument()
    expect(screen.getByText('Euro')).toBeInTheDocument()
  })

  it('should call onChange when selecting', async () => {
    const user = userEvent.setup()
    const onChange = jest.fn()
    render(<CurrencySelect value="USD" onChange={onChange} label="From" />)

    const select = screen.getByLabelText('From')
    await user.selectOptions(select, 'BRL')

    expect(onChange).toHaveBeenCalledWith('BRL')
  })

  it('should display selected value', () => {
    const onChange = jest.fn()
    render(<CurrencySelect value="EUR" onChange={onChange} label="To" />)

    const select = screen.getByLabelText('To') as HTMLSelectElement
    expect(select.value).toBe('EUR')
  })
})

