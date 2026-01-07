interface ConvertButtonProps {
  onClick: () => void;
  loading: boolean;
  disabled?: boolean;
}

export default function ConvertButton({ onClick, loading, disabled }: ConvertButtonProps) {
  return (
    <button
      onClick={onClick}
      disabled={loading || disabled}
      className="w-full mt-6 text-white py-3 rounded font-medium text-sm uppercase tracking-wider transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      style={{
        backgroundColor: loading ? '#8ab3cf' : '#4180ab',
      }}
      onMouseEnter={(e) => {
        if (!loading && !disabled) {
          e.currentTarget.style.backgroundColor = '#8ab3cf';
        }
      }}
      onMouseLeave={(e) => {
        if (!loading && !disabled) {
          e.currentTarget.style.backgroundColor = '#4180ab';
        }
      }}
    >
      {loading ? 'Convertendo...' : 'Converter'}
    </button>
  );
}

