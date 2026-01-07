interface SwapButtonProps {
  onClick: () => void;
}

export default function SwapButton({ onClick }: SwapButtonProps) {
  return (
    <div className="flex items-end justify-center md:col-span-1">
      <button
        onClick={onClick}
        className="rounded transition-colors flex-shrink-0"
        style={{
          backgroundColor: '#e4ebf0',
          color: '#000000',
          border: '1px solid #bdd1de',
          padding: '0.75rem',
          height: '3rem',
          width: '3rem',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.backgroundColor = '#bdd1de';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.backgroundColor = '#e4ebf0';
        }}
        title="Trocar moedas"
      >
        ⇄
      </button>
    </div>
  );
}

