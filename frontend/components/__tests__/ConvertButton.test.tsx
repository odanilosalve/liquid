import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ConvertButton from '../ConvertButton'

describe('ConvertButton', () => {
  it('should render with correct text', () => {
    const onClick = jest.fn()
    render(<ConvertButton onClick={onClick} loading={false} />)

    expect(screen.getByText('Convert')).toBeInTheDocument()
  })

  it('should call onClick when clicked', async () => {
    const user = userEvent.setup()
    const onClick = jest.fn()
    render(<ConvertButton onClick={onClick} loading={false} />)

    const button = screen.getByText('Convert')
    await user.click(button)

    expect(onClick).toHaveBeenCalledTimes(1)
  })

  it('should show loading text when loading', () => {
    const onClick = jest.fn()
    render(<ConvertButton onClick={onClick} loading={true} />)

    expect(screen.getByText('Converting...')).toBeInTheDocument()
    expect(screen.queryByText('Convert')).not.toBeInTheDocument()
  })

  it('should be disabled when loading', () => {
    const onClick = jest.fn()
    render(<ConvertButton onClick={onClick} loading={true} />)

    const button = screen.getByText('Converting...')
    expect(button).toBeDisabled()
  })

  it('should be disabled when disabled prop is true', () => {
    const onClick = jest.fn()
    render(<ConvertButton onClick={onClick} loading={false} disabled={true} />)

    const button = screen.getByText('Convert')
    expect(button).toBeDisabled()
  })

  it('should not be disabled when not loading and not disabled', () => {
    const onClick = jest.fn()
    render(<ConvertButton onClick={onClick} loading={false} disabled={false} />)

    const button = screen.getByText('Convert')
    expect(button).not.toBeDisabled()
  })
})

