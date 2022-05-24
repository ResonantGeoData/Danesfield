import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import * as Sentry from '@sentry/vue';
import { createApp, } from 'vue';
import { createRouter } from 'vue-router';
import { createVuetify } from 'vuetify';
import * as Cesium from 'cesium';

import App from './App.vue';
import { restoreLogin, oauthClient } from './api';
import makeOptions from './router';

// Set token to empty string to avoid warning
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
Cesium.Ion.defaultAccessToken = '';

const app = createApp(App);
const Vuetify = createVuetify({
  components,
  directives,
});

restoreLogin().then(() => {
  /*
  The router must not be initialized until after the oauth flow is complete, because it
  stores the initial history state at the time of its construction, and we don't want it
  to capture that initial state until after we remove any OAuth response params from the URL.
  */
  const router = createRouter(makeOptions());

  if (import.meta.env.VUE_APP_SENTRY_DSN && window.location.hostname !== 'localhost') {
    Sentry.init({
      app,
      dsn: import.meta.env.VUE_APP_SENTRY_DSN as string,
      release: __COMMIT_HASH__,
    });
  }

  app.use(router);
  app.use(Vuetify);
  app.provide('oauthClient', oauthClient);
  // Object.assign(axiosInstance.defaults.headers.common, oauthClient.authHeaders);
  app.mount('#app');
});
