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

export default defineComponent({
  name: 'CesiumViewer',
  setup() {
    const properties = ref();
    const dialog = ref(false);
    onMounted(async () => {
      // Create ProviderViewModel based on different imagery sources
      // - these can be used without Cesium Ion
      const imageryViewModels = [];

      /* Stamen's website (http://maps.stamen.com) as of 2019-08-28 says that the
       * maps they host may be used free of charge.  For http access, use a url like
       * http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png */
      const StamenAttribution = 'Map tiles by <a href="http://stamen.com">Stamen '
        + 'Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">'
        + 'CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap'
        + '</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.';

      /* Per Carto's website regarding basemap attribution: https://carto.com/help/working-with-data/attribution/#basemaps */
      const CartoAttribution = 'Map tiles by <a href="https://carto.com">Carto</a>, under CC BY 3.0. Data by <a href="https://www.openstreetmap.org/">OpenStreetMap</a>, under ODbL.';

      imageryViewModels.push(new Cesium.ProviderViewModel({
        name: 'OpenStreetMap',
        iconUrl: Cesium.buildModuleUrl('Widgets/Images/ImageryProviders/openStreetMap.png'),
        tooltip: 'OpenStreetMap (OSM) is a collaborative project to create a free editable map of the world.\nhttp://www.openstreetmap.org',
        creationFunction() {
          return new Cesium.UrlTemplateImageryProvider({
            url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            subdomains: 'abc',
            minimumLevel: 0,
            maximumLevel: 19,
          });
        },
      }));
      imageryViewModels.push(new Cesium.ProviderViewModel({
        name: 'Positron',
        tooltip: 'CartoDB Positron basemap',
        iconUrl: 'http://a.basemaps.cartocdn.com/light_all/5/15/12.png',
        creationFunction() {
          return new Cesium.UrlTemplateImageryProvider({
            url: 'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
            credit: CartoAttribution,
            minimumLevel: 0,
            maximumLevel: 18,
          });
        },
      }));
      imageryViewModels.push(new Cesium.ProviderViewModel({
        name: 'Positron without labels',
        tooltip: 'CartoDB Positron without labels basemap',
        iconUrl: 'http://a.basemaps.cartocdn.com/rastertiles/light_nolabels/5/15/12.png',
        creationFunction() {
          return new Cesium.UrlTemplateImageryProvider({
            url: 'https://{s}.basemaps.cartocdn.com/rastertiles/light_nolabels/{z}/{x}/{y}.png',
            credit: CartoAttribution,
            minimumLevel: 0,
            maximumLevel: 18,
          });
        },
      }));
      imageryViewModels.push(new Cesium.ProviderViewModel({
        name: 'Dark Matter',
        tooltip: 'CartoDB Dark Matter basemap',
        iconUrl: 'http://a.basemaps.cartocdn.com/rastertiles/dark_all/5/15/12.png',
        creationFunction() {
          return new Cesium.UrlTemplateImageryProvider({
            url: 'https://{s}.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}.png',
            credit: CartoAttribution,
            minimumLevel: 0,
            maximumLevel: 18,
          });
        },
      }));
      imageryViewModels.push(new Cesium.ProviderViewModel({
        name: 'Dark Matter without labels',
        tooltip: 'CartoDB Dark Matter without labels basemap',
        iconUrl: 'http://a.basemaps.cartocdn.com/rastertiles/dark_nolabels/5/15/12.png',
        creationFunction() {
          return new Cesium.UrlTemplateImageryProvider({
            url: 'https://{s}.basemaps.cartocdn.com/rastertiles/dark_nolabels/{z}/{x}/{y}.png',
            credit: CartoAttribution,
            minimumLevel: 0,
            maximumLevel: 18,
          });
        },
      }));
      imageryViewModels.push(new Cesium.ProviderViewModel({
        name: 'Voyager',
        tooltip: 'CartoDB Voyager basemap',
        iconUrl: 'http://a.basemaps.cartocdn.com/rastertiles/voyager_labels_under/5/15/12.png',
        creationFunction() {
          return new Cesium.UrlTemplateImageryProvider({
            url: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}.png',
            credit: CartoAttribution,
            minimumLevel: 0,
            maximumLevel: 18,
          });
        },
      }));
      imageryViewModels.push(new Cesium.ProviderViewModel({
        name: 'Voyager without labels',
        tooltip: 'CartoDB Voyager without labels basemap',
        iconUrl: 'http://a.basemaps.cartocdn.com/rastertiles/voyager_nolabels/5/15/12.png',
        creationFunction() {
          return new Cesium.UrlTemplateImageryProvider({
            url: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}.png',
            credit: CartoAttribution,
            minimumLevel: 0,
            maximumLevel: 18,
          });
        },
      }));
      imageryViewModels.push(new Cesium.ProviderViewModel({
        name: 'National Map Satellite',
        iconUrl: 'https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/4/6/4',
        creationFunction() {
          return new Cesium.UrlTemplateImageryProvider({
            url: 'https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}',
            credit: 'Tile data from <a href="https://basemap.nationalmap.gov/">USGS</a>',
            minimumLevel: 0,
            maximumLevel: 16,
          });
        },
      }));
      imageryViewModels.push(new Cesium.ProviderViewModel({
        name: 'Stamen Terrain',
        iconUrl: 'https://stamen-tiles-a.a.ssl.fastly.net/terrain/5/15/12.png',
        creationFunction() {
          return new Cesium.UrlTemplateImageryProvider({
            url: 'https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png',
            credit: StamenAttribution,
            subdomains: 'abcd',
            minimumLevel: 0,
            maximumLevel: 14,
          });
        },
      }));
      imageryViewModels.push(new Cesium.ProviderViewModel({
        name: 'Stamen Terrain Background',
        iconUrl: 'https://stamen-tiles-a.a.ssl.fastly.net/terrain-background/5/15/12.png',
        creationFunction() {
          return new Cesium.UrlTemplateImageryProvider({
            url: 'https://stamen-tiles-{s}.a.ssl.fastly.net/terrain-background/{z}/{x}/{y}.png',
            credit: StamenAttribution,
            subdomains: 'abcd',
            minimumLevel: 0,
            maximumLevel: 14,
          });
        },
      }));
      imageryViewModels.push(new Cesium.ProviderViewModel({
        name: 'Stamen Toner',
        iconUrl: 'https://stamen-tiles-a.a.ssl.fastly.net/toner/5/15/12.png',
        creationFunction() {
          return new Cesium.UrlTemplateImageryProvider({
            url: 'https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
            credit: StamenAttribution,
            subdomains: 'abcd',
            minimumLevel: 0,
            maximumLevel: 14,
          });
        },
      }));
      imageryViewModels.push(new Cesium.ProviderViewModel({
        name: 'Stamen Toner Lite',
        iconUrl: 'https://stamen-tiles-a.a.ssl.fastly.net/toner-lite/5/15/12.png',
        creationFunction() {
          return new Cesium.UrlTemplateImageryProvider({
            url: 'https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.png',
            credit: StamenAttribution,
            subdomains: 'abcd',
            minimumLevel: 0,
            maximumLevel: 14,
          });
        },
      }));

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
