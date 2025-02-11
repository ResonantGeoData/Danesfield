import { Rectangle, UrlTemplateImageryProvider } from 'cesium';
import { ref, watch } from 'vue';
import {
  rgdImageTilesMeta, rgdCreateUrl,
  rgdTokenSignature, rgdImagery,
} from '@/api';
import { TileParamsType } from '@/store/types';

import { cesiumViewer } from '@/store/cesium';

export const visibleOverlayIds = ref<number[]>();

export const tileImageParams: Record<string, TileParamsType> = {};

const tileLayers: Record<string, {alpha: number}> = {}; // Cesium.TileLayer

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const addVisibleOverlay = (spatialId: number) => {
  if (visibleOverlayIds.value === undefined) {
    visibleOverlayIds.value = [];
  }
  visibleOverlayIds.value.push(spatialId);
};

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export const removeVisibleOverlay = (spatialId: number, region?: boolean) => {
  visibleOverlayIds.value = visibleOverlayIds.value?.filter((obj: number) => obj !== spatialId);
};

const generateTileProvider = async (imageId: number, index = 0) => {
  const data = await rgdImageTilesMeta(imageId);
  const tileSignature = await rgdTokenSignature(); // may need await
  const extents = data.bounds;
  const rectangle = Rectangle.fromDegrees(extents.xmin, extents.ymin, extents.xmax, extents.ymax);
  const tileProvider = new UrlTemplateImageryProvider({
    url: rgdCreateUrl(`rgd_imagery/tiles/${imageId}/tiles/{z}/{x}/{y}.png?projection=EPSG:3857&band=${index}&signature=${tileSignature}`),
    subdomains: [], // We do not need or provide this in RGD
    rectangle,
  });
  return tileProvider;
};

const removeTileLayer = (spatialId: number) => {
  const layers = cesiumViewer.value.scene.imageryLayers;
  layers.remove(tileLayers[spatialId]);
  delete tileLayers[spatialId];
};

export const updateTileLayer = async (spatialId: number) => {
  if (!visibleOverlayIds.value) {
    return;
  }
  const imageId = tileImageParams[spatialId].image.id;
  const { index } = tileImageParams[spatialId];

  // Purge existing tile layer for this ID
  if (visibleOverlayIds.value.indexOf(spatialId) < 0) {
    removeTileLayer(spatialId);
  }

  // Update tile layer for this ID - given imageId and band
  if (visibleOverlayIds.value.indexOf(spatialId) >= 0) {
    const tileProvider = await generateTileProvider(imageId, index);
    const layers = cesiumViewer.value.scene.imageryLayers;
    layers.remove(tileLayers[spatialId]);
    const tileLayer = layers.addImageryProvider(tileProvider);
    tileLayers[spatialId] = tileLayer;
  }
};

export const updateTileLayerOpacity = (spatialId: number, value: number) => {
  const tileLayer = tileLayers[spatialId];
  tileLayer.alpha = value;
};

watch(visibleOverlayIds, () => {
  if (!visibleOverlayIds.value) {
    return;
  }
  // Remove layers not supposed to be visible
  Object.keys(tileImageParams).forEach((key: string) => {
    const spatialId = Number(key);
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    if (visibleOverlayIds.value!.indexOf(spatialId) < 0) {
      removeTileLayer(spatialId);
      delete tileImageParams[spatialId];
    }
  });

  // Add visible layers not present
  // eslint-disable-next-line no-unused-expressions
  visibleOverlayIds.value?.forEach(async (spatialId: number) => {
    if (!(spatialId in tileImageParams)) {
      const result = await rgdImagery(spatialId);
      tileImageParams[spatialId] = {
        image: {
          id: result.parent_raster.image_set.images[0].id as unknown as number,
          name: result.parent_raster.image_set.images[0].file.name,
        },
        index: 0,
        opacity: 1,
      };
      updateTileLayer(spatialId);
    }
  });
}, { deep: true });
