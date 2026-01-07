'use client';

import { useState } from 'react';
import CurrencyConverter from '@/components/CurrencyConverter';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col" style={{ backgroundColor: '#e4ebf0' }}>
      <div className="container mx-auto px-4 py-16 flex-1">
        <CurrencyConverter />
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
