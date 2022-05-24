import axios from 'axios';
import OauthClient from '@girder/oauth-client';
import { GeoJSON, Polygon, MultiPolygon } from 'geojson'; // eslint-disable-line
import { stringify } from 'qs';  // eslint-disable-line
import { reactive } from 'vue';

export const axiosInstance = axios.create({
  baseURL: `${import.meta.env.VUE_APP_API_ROOT}api`,
  paramsSerializer: (params) => stringify(params, { arrayFormat: 'repeat' }),
});
export const oauthClient = reactive(new OauthClient(
  import.meta.env.VUE_APP_OAUTH_API_ROOT as string,
  import.meta.env.VUE_APP_OAUTH_CLIENT_ID as string,
));

export async function restoreLogin() {
  if (!oauthClient) {
    return;
  }
  await oauthClient.maybeRestoreLogin();
}

axiosInstance.interceptors.request.use((config) => ({
  ...config,
  headers: {
    ...oauthClient?.authHeaders,
    ...config.headers,
  },
}));

export async function rgdSearch(
  limit?: number,
  offset?: number,
  q?: Polygon | MultiPolygon,
  predicate?: string | null,
  acquiredBefore?: string | null,
  acquiredAfter?: string | null,
  distanceMin? : string | null,
  distanceMax? : string | null,
  instrumentation?: string | null,
  startTime?: string | null,
  endTime?: string | null,
  collections?: string[] | number[],

) {
  let geometry;
  if (q?.coordinates.length === 0) {
    // Catch if empty geometry is given (the default value for type sanity)
    geometry = undefined;
  } else {
    geometry = q;
  }
  const response = await axiosInstance.get('rgd/search', {
    /* eslint-disable @typescript-eslint/camelcase */
    params: {
      limit,
      offset,
      q: JSON.stringify(geometry),
      predicate,
      acquired_after: acquiredAfter,
      acquired_before: acquiredBefore,
      distance_min: distanceMin,
      distance_max: distanceMax,
      instrumentation,
      time_of_day_after: startTime,
      time_of_day_before: endTime,
      collections,
    },
    /* eslint-enable @typescript-eslint/camelcase */
  });
  return response;
}

export async function rgdSpatialEntry(
  spatialID: number,
) {
  const response = await axiosInstance.get(`rgd/spatial_entry/${spatialID}`);
  return response.data;
}

export async function rgdFootprint(
  spatialID: number,
) {
  const response = await axiosInstance.get<{ footprint: GeoJSON }>(`rgd/spatial_entry/${spatialID}/footprint`);
  return response.data.footprint;
}

export async function rgdImagery(
  spatialID: number,
) {
  const response = await axiosInstance.get(`/rgd_imagery/raster/${spatialID}`);
  return response.data;
}

export async function rgdImageTilesMeta(
  imageId: number,
) {
  const response = await axiosInstance.get(`/rgd_imagery/tiles/${imageId}/metadata`);
  return response.data;
}

export async function rgdTiles3d(
  spatialID: number,
) {
  const response = await axiosInstance.get(`/rgd_3d/tiles3d/${spatialID}`);
  return response.data;
}

export async function rgdTokenSignature() {
  const response = await axiosInstance.post('/signature');
  return response.data.signature;
}

export function rgdHost() {
  const url = new URL(String(axiosInstance.defaults.baseURL));
  return url.host;
}

export function rgdBaseUrl() {
  return axiosInstance.defaults.baseURL;
}

export function rgdCreateUrl(path: string) {
  return `${rgdBaseUrl()}/${path}`;
}

export async function imageryBands(
  spatialID: number,
) {
  const response = await axiosInstance.get(`/rgd_imagery/tiles/${spatialID}/bands`);

  return response;
}
