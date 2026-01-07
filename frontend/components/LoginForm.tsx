'use client';

import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';

export default function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      await login(username, password);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center z-50" style={{ backgroundColor: 'rgba(0, 0, 0, 0.5)' }}>
      <div className="max-w-md w-full mx-4">
        <div className="rounded-lg p-8 shadow-lg" style={{ backgroundColor: '#ffffff', border: '1px solid #e4ebf0' }}>
          <h2 className="text-2xl font-semibold mb-6 text-center" style={{ color: '#000000' }}>
            Login
          </h2>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username"
                required
                className="w-full px-4 py-3 border rounded focus:outline-none focus:ring-2"
                style={{
                  borderColor: '#bdd1de',
                  color: '#000000',
                  backgroundColor: '#ffffff',
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#4180ab';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = '#bdd1de';
                }}
              />
            </div>

            <div>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                required
                className="w-full px-4 py-3 border rounded focus:outline-none focus:ring-2"
                style={{
                  borderColor: '#bdd1de',
                  color: '#000000',
                  backgroundColor: '#ffffff',
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#4180ab';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = '#bdd1de';
                }}
              />
            </div>

            {error && (
              <div className="p-3 rounded" style={{ backgroundColor: '#fee', color: '#c00' }}>
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              style={{
                backgroundColor: loading ? '#8ab3cf' : '#4180ab',
                color: '#ffffff',
              }}
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

