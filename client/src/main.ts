import Vue from 'vue';
import { Ion as CesiumIon } from 'cesium';
import * as Sentry from '@sentry/vue';

// Composition plugin must be the first local import
import '@/plugins/composition';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import { restoreLogin, oauthClient, axiosInstance } from './api';

// Set token to `null` to avoid warning
CesiumIon.defaultAccessToken = '';

Sentry.init({
  Vue,
  dsn: process.env.VUE_APP_SENTRY_DSN,
});

async function login() {
  return restoreLogin();
}

login().then(() => {
  new Vue({
    provide: {
      axios: axiosInstance,
      oauthClient,
    },
    router,
    vuetify,
    render: (h) => h(App),
  }).$mount('#app');
});
