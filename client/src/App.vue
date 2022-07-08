<script lang="ts">
import {
  computed, defineComponent, ref,
} from 'vue';
import { axiosInstance, oauthClient } from '@/api';

import router from '@/router';

export default defineComponent({
  setup() {
    const loginText = computed(() => (oauthClient.isLoggedIn ? 'Logout' : 'Login'));
    const logInOrOut = () => {
      if (oauthClient.isLoggedIn) {
        oauthClient.logout();
      } else {
        oauthClient.redirectToLogin();
      }
    };

    // Link for girder tab
    const apiLink = `${axiosInstance.defaults.baseURL}/docs/swagger`;
    const tab = computed(() => router.currentRoute.path);

    // onTabChange is only called when the api link is clicked.
    // Once clicked, set value back to what it should be.
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const tabsRef = ref<any>(null);
    function onTabChange() {
      const itemsComponent = tabsRef.value.$refs.items;
      itemsComponent.internalValue = tab.value;
    }

    return {
      loginText,
      logInOrOut,
      tab,
      tabsRef,
      apiLink,
      onTabChange,
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
        no-gutters
      >
        <v-app-bar-title>
          <v-avatar tile>
            <img src="../public/icon_large.png">
          </v-avatar>
          Danesfield
        </v-app-bar-title>
      </v-row>

      <v-tabs
        ref="tabsRef"
        :value="tab"
        icons-and-text
        class="mx-3"
        @change="onTabChange"
      >
        <v-tab to="/explore">
          Explore
          <v-icon>mdi-compass</v-icon>
        </v-tab>
        <v-tab to="/tasks">
          Tasks
          <v-icon>mdi-list-status</v-icon>
        </v-tab>
        <v-tab
          :href="apiLink"
          target="_blank"
          rel="noopener noreferrer"
        >
          API Docs
          <v-icon>mdi-open-in-new</v-icon>
        </v-tab>
      </v-tabs>
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
