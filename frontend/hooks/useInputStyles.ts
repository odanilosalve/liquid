import { useState } from 'react';

export function useInputStyles() {
  const [focused, setFocused] = useState(false);

  const styles = {
    border: `1px solid ${focused ? '#000000' : '#e4ebf0'}`,
    backgroundColor: '#ffffff',
    color: '#000000',
  };

  const onFocus = () => setFocused(true);
  const onBlur = () => setFocused(false);

  return { styles, onFocus, onBlur };
}


