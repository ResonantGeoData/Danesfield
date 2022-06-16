<script lang="ts">
import 'cesium/Build/Cesium/Widgets/widgets.css';
import {
  defineComponent,
  onMounted,
  PropType,
  ref,
} from '@vue/composition-api';
import { cesiumViewer } from '@/store/cesium';
import { Camera, Viewer } from 'cesium';
import { imageryViewModels } from '@/utils/cesium';
import type { Polygon } from 'geojson';  // eslint-disable-line

export default defineComponent({
  name: 'CesiumViewer',
  props: {
    footprints: {
      type: Object as PropType<Partial<Record<number, Polygon>>>,
      default: null,
    },
  },
  setup() {
    const properties = ref();
    const dialog = ref(false);

    onMounted(() => {
      // Initialize the viewer - this works without a token
      cesiumViewer.value = new Viewer('cesiumContainer', {
        // imageryProvider: false,
        imageryProviderViewModels: imageryViewModels,
        selectedImageryProviderViewModel: imageryViewModels[5], // Voyager
        animation: true,
        shouldAnimate: true,
        timeline: true,
        infoBox: false,
        homeButton: false,
        fullscreenButton: false,
        selectionIndicator: false,
        geocoder: false,
      });
      // Remove the Terrain section of the baseLayerPicker
      cesiumViewer.value.baseLayerPicker.viewModel.terrainProviderViewModels.removeAll();

      cesiumViewer.value.forceResize();
      Camera.DEFAULT_VIEW_FACTOR = 0;
    });

    return {
      dialog,
      properties,
    };
  },
});
</script>

<template>
  <div id="cesiumContainer" />
</template>

<style>
#cesiumContainer{
  width: 100% !important;
  height: calc(100vh - 48px) !important;
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
