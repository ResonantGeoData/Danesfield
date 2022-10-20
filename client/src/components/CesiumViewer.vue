<script setup lang="ts">
import 'cesium/Build/Cesium/Widgets/widgets.css';
import { onMounted } from 'vue';
import type { PropType } from 'vue';
import * as Cesium from 'cesium';
import { cesiumViewer } from '@/store/cesium';
import { imageryViewModels } from '@/utils/cesium';
import type { Polygon } from 'geojson';  // eslint-disable-line

const CESIUM_API_KEY: string | undefined = process.env.VUE_APP_CESIUM_ION_API_KEY;

if (CESIUM_API_KEY) {
  Cesium.Ion.defaultAccessToken = CESIUM_API_KEY;
}

defineProps({
  footprints: {
    type: Object as PropType<Partial<Record<number, Polygon>>>,
    default: null,
  },
});

onMounted(async () => {
  // Initialize the CesiumJS viewer
  cesiumViewer.value = await new Cesium.Viewer('cesiumContainer', {
    imageryProviderViewModels: CESIUM_API_KEY ? undefined : imageryViewModels,
    terrainProvider: CESIUM_API_KEY ? Cesium.createWorldTerrain() : undefined,
    animation: true,
    shouldAnimate: true,
    timeline: true,
    infoBox: false,
    homeButton: false,
    fullscreenButton: false,
    selectionIndicator: false,
    geocoder: false,
  });

  // Remove terrain layer if a Cesium Ion token isn't available. Otherwise,
  // even the imagery layer won't render if you don't specify a key.
  if (!CESIUM_API_KEY) {
    cesiumViewer.value.baseLayerPicker.viewModel.terrainProviderViewModels.removeAll();
  }

  cesiumViewer.value.forceResize();
  Cesium.Camera.DEFAULT_VIEW_FACTOR = 0;
});

</script>

<template>
  <div id="cesiumContainer" />
</template>

<style>
#cesiumContainer{
  width: 100% !important;
  cursor: grab;
}
#cesiumContainer.draw-mode{
  cursor: crosshair
}
.cesium-viewer-timelineContainer {
  height: 50px;
  font-size: 20px;
}
.cesium-timeline-main {
  border: none;
}
.cesium-timeline-bar {
  cursor: pointer;
  height: 3em;
  background-color: #1E1E1E;
}
.cesium-timeline-needle {
  top: 1em;
  width: 2px;
}
.cesium-timeline-icon16 {
  background-image: none;
}

.cesium-widget-credits {
    display: none !important;
}
</style>
