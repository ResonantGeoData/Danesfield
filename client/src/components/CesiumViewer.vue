<script lang="ts">
import {
  defineComponent,
  onMounted,
  ref,
}
  from '@vue/composition-api';
import Cesium from '@/plugins/cesium';
import { cesiumViewer, getSelectedEntityFromPoint } from '@/store/cesium/index';
import { useMap } from '@/store/cesium/search';
import { Clock, JulianDate } from 'cesium';
import { searchParameters } from '@/store/search';
import { imageryViewModels } from '@/utils/cesium';

export default defineComponent({
  name: 'CesiumViewer',
  setup() {
    const properties = ref();
    const dialog = ref(false);
    onMounted(async () => {
      // Initialize the viewer - this works without a token
      cesiumViewer.value = new Cesium.Viewer('cesiumContainer', {
        // imageryProvider: false,
        imageryProviderViewModels: imageryViewModels,
        selectedImageryProviderViewModel: imageryViewModels[5], // Voyager
        animation: false,
        timeline: true,
        infoBox: false,
        homeButton: false,
        fullscreenButton: false,
        selectionIndicator: false,
        geocoder: false,
      });
      // Viewer.clock is read-only, but we can set its values and zoom to them
      cesiumViewer.value.clock.startTime = Cesium.JulianDate.fromIso8601('2012-12-25');
      cesiumViewer.value.clock.currentTime = Cesium.JulianDate.fromIso8601('2015-12-25');
      cesiumViewer.value.clock.stopTime = Cesium.JulianDate.now();
      cesiumViewer.value.timeline.updateFromClock();
      cesiumViewer.value.timeline.zoomTo(
        cesiumViewer.value.clock.startTime,
        cesiumViewer.value.clock.stopTime,
      );

      const SELECTED_DATE_MARGIN_DAYS = 10;

      cesiumViewer.value.timeline.addEventListener(
        'settime',
        ({ clock }: Record<string, Clock>) => {
          const julian: JulianDate = clock.currentTime;
          // const currentDate: Date = new Date(julian.toString());
          // const startDate = currentDate;
          // startDate.setDate(currentDate.getDate() - SELECTED_DATE_MARGIN_DAYS);
          // const endDate = currentDate;
          // endDate.setDate(currentDate.getDate() + SELECTED_DATE_MARGIN_DAYS);
          // const toFormattedDateString = (date: Date) => {
          //   const YYYY = date.getUTCFullYear();
          //   const MM = (date.getUTCMonth() + 1).toString().padStart(2, '0');
          //   const DD = date.getUTCDate().toString().padStart(2, '0');
          //   return `${YYYY}-${MM}-${DD}`; // Needs to be ISO 8601
          // };

          // const startDate = Cesium.JulianDate.addDays(julian, SELECTED_DATE_MARGIN_DAYS);
          // const endDate = Cesium.JulianDate.addDays(julian, -SELECTED_DATE_MARGIN_DAYS);

          const startDate = { ...julian };
          startDate.dayNumber += SELECTED_DATE_MARGIN_DAYS;
          const endDate = { ...julian };
          endDate.dayNumber -= SELECTED_DATE_MARGIN_DAYS;

          searchParameters.value = {
            ...searchParameters.value,
            acquired: {
              ...searchParameters.value.acquired,
              startDate: Cesium.JulianDate.toIso8601(startDate, 0),
              endDate: Cesium.JulianDate.toIso8601(endDate, 0),
            },
          };
        },
        false,
      );
      // Remove the Terrain section of the baseLayerPicker
      cesiumViewer.value.baseLayerPicker.viewModel.terrainProviderViewModels.removeAll();

      cesiumViewer.value.forceResize();
      cesiumViewer.value.camera.setView({
        destination: Cesium.Cartesian3.fromDegrees(-93.849688, 40.690265, 4000000),
      });
      Cesium.Camera.DEFAULT_VIEW_FACTOR = 0;

      // Tooltip handler for showing an entity's properties
      const handlerToolTips = new Cesium.ScreenSpaceEventHandler(cesiumViewer.value.scene.canvas);
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      handlerToolTips.setInputAction((movement: any) => {
        const selectedEntity = getSelectedEntityFromPoint(movement.position);

        if (selectedEntity != null) {
          properties.value = selectedEntity.properties.getValue(Cesium.JulianDate.now());
          dialog.value = true;
          // show pop up tooltip with table of properties
        }
      }, Cesium.ScreenSpaceEventType.LEFT_CLICK);
    });

    return {
      useMap,
      dialog,
      properties,
    };
  },
});
</script>

<template>
  <div
    id="cesiumContainer"
    :class="useMap? 'draw-mode': ''"
  >
    <v-dialog
      v-model="dialog"
      open-on-hover
      right
      max-width="300px"
    >
      <v-card>
        <v-simple-table
          class="px-5"
        >
          <tbody>
            <tr
              v-for="(value, key) in properties"
              :key="key"
            >
              <td>{{ key }}</td>
              <td>{{ value }}</td>
            </tr>
          </tbody>
        </v-simple-table>
      </v-card>
    </v-dialog>
  </div>
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
</style>
