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
    <div className="max-w-md mx-auto">
      <div className="rounded p-8" style={{ backgroundColor: '#ffffff', border: '1px solid #e4ebf0' }}>
        <h2 className="text-2xl font-semibold mb-6" style={{ color: '#000000' }}>
          Login
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium mb-2" style={{ color: '#000000' }}>
              Username
            </label>
            <input
              id="username"
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2"
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
            <label htmlFor="password" className="block text-sm font-medium mb-2" style={{ color: '#000000' }}>
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2"
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
  );
}

