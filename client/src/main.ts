import Vue from 'vue';
import * as Sentry from '@sentry/vue';

// Composition plugin must be the first local import
import '@/plugins/composition';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';

Sentry.init({
  Vue,
  dsn: process.env.VUE_APP_SENTRY_DSN,
});

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
