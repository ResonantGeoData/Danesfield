import OauthClient from '@girder/oauth-client';
import { reactive } from '@vue/composition-api';
import axios from 'axios';

export const axiosInstance = axios.create({
  baseURL: process.env.VUE_APP_API_ROOT,
});

export const oauthClient = reactive(
  new OauthClient(
    process.env.VUE_APP_OAUTH_API_ROOT,
    process.env.VUE_APP_OAUTH_CLIENT_ID,
  ),
);

oauthClient.maybeRestoreLogin().then(async () => {
  Object.assign(axiosInstance.defaults.headers.common, oauthClient.authHeaders);
});
