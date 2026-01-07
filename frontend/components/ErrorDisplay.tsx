interface ErrorDisplayProps {
  error: string | null;
}

export default function ErrorDisplay({ error }: ErrorDisplayProps) {
  if (!error) return null;

  return (
    <div className="mt-4 p-3 rounded text-sm" style={{ backgroundColor: '#e4ebf0', color: '#000000', border: '1px solid #bdd1de' }}>
      {error}
    </div>
  );
}

