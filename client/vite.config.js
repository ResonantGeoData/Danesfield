
import { defineConfig } from 'vite';
import Vue from '@vitejs/plugin-vue';
import Vuetify from '@vuetify/vite-plugin';
import cesium from 'vite-plugin-cesium';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  base: './',
  envPrefix: 'VUE_APP_',
  define: {
    // Populated by netlify https://docs.netlify.com/configure-builds/environment-variables/
    __COMMIT_HASH__: JSON.stringify(process.env.COMMIT_REF || ''),
  },
  plugins: [
    Vue(),
    Vuetify({
      autoImport: true
    }),
    cesium()
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    }
  },
});
