<script lang="ts">
import { computed, defineComponent } from '@vue/composition-api';
import { oauthClient } from '@/api';

export default defineComponent({
  setup(props, ctx) {
    const router = ctx.root.$router;
    function navigateHome() {
      if (router.currentRoute.path !== '/') {
        router.push('/');
      }
    }

    const loginText = computed(() => (oauthClient.isLoggedIn ? 'Logout' : 'Login'));
    const logInOrOut = () => {
      if (oauthClient.isLoggedIn) {
        oauthClient.logout();
      } else {
        oauthClient.redirectToLogin();
      }
    };

    return {
      loginText,
      logInOrOut,
      navigateHome,
    };
  },
});
</script>

<template>
  <v-app>
    <!-- For some reason, flex-grow-0 is needed or the app-bar is huge -->
    <v-app-bar class="flex-grow-0">
      <v-row
        align="center"
        style="cursor: pointer;"
        @click="navigateHome"
      >
        <v-avatar tile>
          <img src="../public/icon_large.png">
        </v-avatar>
        <span class="ml-2 text-h4 font-weight-regular">
          OASIS
        </span>
      </v-row>
      <v-spacer />
      <v-btn
        text
        @click="logInOrOut"
      >
        {{ loginText }}
      </v-btn>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
