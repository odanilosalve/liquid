import { useInputStyles } from '@/hooks/useInputStyles';
import { CURRENCIES } from '@/constants/currencies';

interface CurrencySelectProps {
  value: string;
  onChange: (value: string) => void;
  label: string;
}

export default function CurrencySelect({ value, onChange, label }: CurrencySelectProps) {
  const { styles, onFocus, onBlur } = useInputStyles();

  return (
    <div className="md:col-span-4">
      <label className="block text-xs uppercase tracking-wider mb-2" style={{ color: '#000000' }}>
        {label}
      </label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-4 py-3 rounded text-lg transition-colors"
        style={styles}
        onFocus={onFocus}
        onBlur={onBlur}
      >
        {CURRENCIES.map((currency) => (
          <option key={currency.code} value={currency.code}>
            {currency.name}
          </option>
        ))}
      </select>
    </div>
  );
}


