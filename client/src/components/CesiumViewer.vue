<script lang="ts">
import 'cesium/Build/Cesium/Widgets/widgets.css';
import {
  defineComponent,
  onMounted,
  PropType,
  ref,
  watch,
} from '@vue/composition-api';
import router from '@/router';
import { addGeojson, cesiumViewer } from '@/store/cesium';
import {
  DataSourceCollection,
  Primitive,
  Entity,
  Cartesian2,
  DataSource,
  ScreenSpaceEventType,
  Cartesian3,
  Camera,
  ScreenSpaceEventHandler,
  Viewer,
} from 'cesium';
import { addPin } from '@/store/cesium/pins';
import { imageryViewModels } from '@/utils/cesium';
import { Polygon } from 'geojson';  // eslint-disable-line
import { centroid } from '@turf/turf';

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
      cesiumViewer.value = new Viewer('cesiumContainer', {
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
      Camera.DEFAULT_VIEW_FACTOR = 0;

      const handler = new ScreenSpaceEventHandler(cesiumViewer.value.scene.canvas);
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
      }, ScreenSpaceEventType.LEFT_CLICK);
    });

    // Add footprints/pins to globe
    watch(() => props.footprints, (newFootprints) => {
      Object.values(newFootprints).forEach((footprint, i) => {
        if (!footprint?.coordinates) {
          return;
        }
        const [x, y] = centroid(footprint).geometry.coordinates;
        addPin(Cartesian3.fromDegrees(x, y), i); // add pin to dataset location to globe
        addGeojson(footprint); // add dataset footprint to globe
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
