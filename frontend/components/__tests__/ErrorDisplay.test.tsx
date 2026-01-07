import { render, screen } from '@testing-library/react'
import ErrorDisplay from '../ErrorDisplay'

describe('ErrorDisplay', () => {
  it('should not render when error is null', () => {
    const { container } = render(<ErrorDisplay error={null} />)
    expect(container.firstChild).toBeNull()
  })

  it('should not render when error is empty string', () => {
    const { container } = render(<ErrorDisplay error="" />)
    expect(container.firstChild).toBeNull()
  })

  it('should render error message when error exists', () => {
    render(<ErrorDisplay error="Currency conversion error" />)

    expect(screen.getByText('Currency conversion error')).toBeInTheDocument()
  })

  it('should display different error messages', () => {
    const { rerender } = render(<ErrorDisplay error="First error" />)
    expect(screen.getByText('First error')).toBeInTheDocument()

    rerender(<ErrorDisplay error="Second error" />)
    expect(screen.getByText('Second error')).toBeInTheDocument()
  })
})

