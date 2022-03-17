import Cesium from '@/plugins/cesium';
import { GeoJsonDataSource } from 'cesium';
import { ref, watch } from '@vue/composition-api';
import { cesiumViewer, addGeojson } from '@/store/cesium';
import { rgdFootprint, rgdRegionSites } from '@/api/rest';
import { GeoJSON } from 'geojson';  // eslint-disable-line

export const visibleFootprints = ref<Record<string, GeoJSON >>({});

export const addFootprint = async (spatialId: number, region?: boolean) => {
  let key;
  let footprint;
  if (!region) {
    footprint = (await rgdFootprint(spatialId));
    key = `result_${spatialId}`;
  } else {
    footprint = await rgdRegionSites(spatialId);
    key = `region_${spatialId}`;
  }
  if (key && footprint) {
    visibleFootprints.value = { ...visibleFootprints.value, [key]: footprint };
  }
};

export const removeFootprint = (spatialId: number, region?: boolean) => {
  let key: string;
  if (!region) {
    key = `result_${spatialId}`;
  } else {
    key = `region_${spatialId}`;
  }
  if (visibleFootprints.value[key]) {
    visibleFootprints.value = Object.fromEntries(
      Object.entries(visibleFootprints.value).filter(([k]) => k !== key),
    );
  }
};

const footprintSources: Record<string, GeoJsonDataSource> = {};

watch(visibleFootprints, (newFootprints, oldFootprints) => {
  Object.keys(oldFootprints).forEach(
    (key) => {
      if (!Object.keys(newFootprints).includes(key)) {
        // remove footprint
        if (key in footprintSources) {
          cesiumViewer.value.dataSources.remove(footprintSources[key]);
          delete footprintSources[key];
        }
      }
    },
  );
  Object.entries(newFootprints).forEach(
    async ([key, footprint]) => {
      if (!Object.keys(oldFootprints).includes(key)) {
        // add footprint
        footprintSources[key] = await addGeojson(footprint);
        cesiumViewer.value.flyTo(footprintSources[key], {
          offset: new Cesium.HeadingPitchRange(
            Cesium.Math.toRadians(0),
            Cesium.Math.toRadians(-90.0),
          ),
        });
      }
    },
  );
});
