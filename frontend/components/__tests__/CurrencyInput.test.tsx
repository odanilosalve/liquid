import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import CurrencyInput from '../CurrencyInput'

describe('CurrencyInput', () => {
  it('should render with label and value', () => {
    const onChange = jest.fn()
    render(<CurrencyInput value="100" onChange={onChange} label="Amount" />)

    expect(screen.getByLabelText('Amount')).toBeInTheDocument()
    expect(screen.getByDisplayValue('100')).toBeInTheDocument()
  })

  it('should call onChange when typing', async () => {
    const user = userEvent.setup()
    const onChange = jest.fn()
    render(<CurrencyInput value="" onChange={onChange} label="Amount" />)

    const input = screen.getByLabelText('Amount')
    await user.type(input, '200')

    expect(onChange).toHaveBeenCalled()
  })

  it('should have correct input attributes', () => {
    const onChange = jest.fn()
    render(<CurrencyInput value="100" onChange={onChange} label="Amount" />)

    const input = screen.getByLabelText('Amount')
    expect(input).toHaveAttribute('type', 'number')
    expect(input).toHaveAttribute('min', '0')
    expect(input).toHaveAttribute('step', '0.01')
    expect(input).toHaveAttribute('placeholder', '0.00')
  })
})

