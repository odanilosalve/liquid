import { ConversionResult as ConversionResultType } from '@/types/conversion';
import { formatCurrency, formatRate } from '@/utils/formatters';

interface ConversionResultProps {
  result: ConversionResultType;
  getCurrencyInfo: (code: string) => { code: string; name: string };
}

export default function ConversionResult({ result, getCurrencyInfo }: ConversionResultProps) {
  return (
    <div className="rounded-lg p-8 mb-6" style={{ backgroundColor: '#ffffff', border: '1px solid #bdd1de' }}>
      <div className="grid md:grid-cols-2 gap-8 mb-8">
        <div>
          <div className="text-xs uppercase tracking-wider mb-2" style={{ color: '#000000' }}>Original Amount</div>
          <div className="text-3xl font-light" style={{ color: '#000000' }}>
            {formatCurrency(result.amount)} <span className="text-lg" style={{ color: '#000000' }}>{getCurrencyInfo(result.from).name}</span>
          </div>
        </div>

        <div>
          <div className="text-xs uppercase tracking-wider mb-2" style={{ color: '#000000' }}>Converted Amount</div>
          <div className="text-3xl font-light" style={{ color: '#000000' }}>
            {formatCurrency(result.converted_amount)} <span className="text-lg" style={{ color: '#000000' }}>{getCurrencyInfo(result.to).name}</span>
          </div>
        </div>
      </div>

      <div className="pt-6 border-t" style={{ borderColor: '#e4ebf0' }}>
        <div className="text-xs uppercase tracking-wider mb-2 text-center" style={{ color: '#000000' }}>Exchange Rate</div>
        <div className="text-lg font-light text-center" style={{ color: '#000000' }}>
          1 {getCurrencyInfo(result.from).name} = {formatRate(result.rate)} {getCurrencyInfo(result.to).name}
        </div>
      </div>
    </div>
  );
}

