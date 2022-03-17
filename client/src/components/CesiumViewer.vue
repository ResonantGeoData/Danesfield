<script lang="ts">
import {
  defineComponent,
  onMounted,
  PropType,
  ref,
  watch,
}
  from '@vue/composition-api';
import Cesium from '@/plugins/cesium';
import router from '@/router';
import { addGeojson, cesiumViewer } from '@/store/cesium';
import {
  DataSourceCollection, Primitive, Entity, Cartesian2, DataSource,
} from 'cesium';
import { imageryViewModels } from '@/utils/cesium';
import {  Polygon } from 'geojson';  // eslint-disable-line

import { area, polygon, transformScale } from '@turf/turf';

export default defineComponent({
  name: 'CesiumViewer',
  props: {
    footprints: {
      type: Object as PropType<Partial<Record<number, Polygon>>>,
      default: null,
    },
  },
  setup(props) {
    const properties = ref();
    const dialog = ref(false);

    onMounted(async () => {
      // Initialize the viewer - this works without a token
      cesiumViewer.value = new Cesium.Viewer('cesiumContainer', {
        // imageryProvider: false,
        imageryProviderViewModels: imageryViewModels,
        selectedImageryProviderViewModel: imageryViewModels[5], // Voyager
        animation: false,
        timeline: false,
        infoBox: false,
        homeButton: false,
        fullscreenButton: false,
        selectionIndicator: false,
        geocoder: false,
      });
      // Remove the Terrain section of the baseLayerPicker
      cesiumViewer.value.baseLayerPicker.viewModel.terrainProviderViewModels.removeAll();

      cesiumViewer.value.forceResize();
      cesiumViewer.value.camera.setView({
        destination: Cesium.Cartesian3.fromDegrees(-93.849688, 40.690265, 4000000),
      });
      Cesium.Camera.DEFAULT_VIEW_FACTOR = 0;

      const handler = new Cesium.ScreenSpaceEventHandler(cesiumViewer.value.scene.canvas);
      handler.setInputAction((movement: {position: Cartesian2}) => {
        const pickedObject: { primitive: Primitive; id: Entity } = cesiumViewer.value.scene.pick(
          movement.position,
        );
        const datasources: DataSourceCollection = cesiumViewer.value.dataSources;

        const clickedEntity = pickedObject.id;

        let geoJsonSource: DataSource;
        for (let i = 0; i < datasources.length; i += 1) {
          geoJsonSource = datasources.get(i);
          if (geoJsonSource.name === clickedEntity.properties?.name.getValue()) {
            break;
          }
        }

        Object.entries(props.footprints).forEach(([datasetId, footprint]) => {
          if (JSON.stringify(footprint) === geoJsonSource.name) {
            router.push({ name: 'focus', params: { datasetId } });
          }
        });
      }, Cesium.ScreenSpaceEventType.LEFT_CLICK);
    });

    watch(() => props.footprints, (newFootprints) => {
      // Scale up footprint size so they're visible from space
      Object.values(newFootprints).forEach((footprint) => {
        if (!footprint?.coordinates) {
          return;
        }
        const poly = polygon(footprint.coordinates);

        let scale = 1;
        let scaledPoly;
        while (true) {
          scaledPoly = transformScale(poly, scale);
          if (area(scaledPoly) >= 10000000000) {
            break;
          }
          scale += 1;
        }
        // eslint-disable-next-line no-param-reassign
        footprint.coordinates = scaledPoly.geometry.coordinates;
      });
      Object.values(newFootprints).forEach((footprint: any) => {
        addGeojson(footprint);
      });
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
