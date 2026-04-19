import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: true, // Permite que o Codespaces exponha a porta
    port: 5173, // Fixa a porta padrão do Vite
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // Usa IP local para evitar problemas de DNS
        changeOrigin: true,
        secure: false,
      },
    },
  },
});