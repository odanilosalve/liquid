'use client';

import { useAuth } from '@/contexts/AuthContext';
import CurrencyConverter from '@/components/CurrencyConverter';
import LoginForm from '@/components/LoginForm';

export default function Home() {
  const { isAuthenticated, loading, logout, user } = useAuth();

  if (loading) {
    return (
      <main className="min-h-screen flex flex-col items-center justify-center" style={{ backgroundColor: '#e4ebf0' }}>
        <div style={{ color: '#000000' }}>Loading...</div>
      </main>
    );
  }

  return (
    <main className="min-h-screen flex flex-col" style={{ backgroundColor: '#e4ebf0' }}>
      {isAuthenticated && (
        <div className="container mx-auto px-4 pt-4">
          <div className="flex justify-between items-center mb-4">
            <div style={{ color: '#000000' }}>
              Hello, <strong>{user?.username}</strong>
            </div>
            <button
              onClick={logout}
              className="px-4 py-2 rounded text-sm font-medium transition-colors"
              style={{
                backgroundColor: '#8ab3cf',
                color: '#ffffff',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = '#bdd1de';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = '#8ab3cf';
              }}
            >
              Logout
            </button>
          </div>
        </div>
      )}
      <div className="container mx-auto px-4 py-16 flex-1">
        {isAuthenticated ? <CurrencyConverter /> : <LoginForm />}
      </div>
      <footer className="py-6" style={{ backgroundColor: '#4180ab' }}>
        <div className="container mx-auto px-4">
          <div className="flex justify-center items-center gap-6 text-sm">
            <a
              href="https://github.com/odanilosalve/liquid"
              target="_blank"
              rel="noopener noreferrer"
              className="transition-colors hover:opacity-70"
              style={{ color: '#ffffff' }}
            >
              GitHub
            </a>
            <span style={{ color: '#ffffff', opacity: 0.7 }}>|</span>
            <a
              href="https://www.linkedin.com/in/danilosalve/"
              target="_blank"
              rel="noopener noreferrer"
              className="transition-colors hover:opacity-70"
              style={{ color: '#ffffff' }}
            >
              LinkedIn
            </a>
          </div>
        </div>
      </footer>
    </main>
  );
}
