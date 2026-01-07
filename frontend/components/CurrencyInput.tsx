import { useInputStyles } from '@/hooks/useInputStyles';

interface CurrencyInputProps {
  value: string;
  onChange: (value: string) => void;
  label: string;
}

export default function CurrencyInput({ value, onChange, label }: CurrencyInputProps) {
  const { styles, onFocus, onBlur } = useInputStyles();

  return (
    <div className="md:col-span-2">
      <label className="block text-xs uppercase tracking-wider mb-2" style={{ color: '#000000' }}>
        {label}
      </label>
      <input
        type="number"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-4 py-3 rounded text-lg transition-colors"
        style={styles}
        onFocus={onFocus}
        onBlur={onBlur}
        placeholder="0.00"
        min="0"
        step="0.01"
      />
    </div>
  );
}

