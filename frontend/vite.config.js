import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',    // Libera o acesso externo (essencial pro Docker)
    port: 5173,         // A porta padrão
    allowedHosts: ['marombai.app', 'www.marombai.app', 'localhost', '148.230.77.18'], //Libera o marombai.app
  },
})