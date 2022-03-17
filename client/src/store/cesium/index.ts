import Cesium from '@/plugins/cesium';
import { ref } from '@vue/composition-api';
import { GeoJSON } from 'geojson';  // eslint-disable-line
import { GeoJsonDataSource } from 'cesium';

// Limit the tile requests on RGD server so that Vue app's requests aren't hung
// Cesium.RequestScheduler.requestsByServer = {
//   host: 3,
// };
Cesium.RequestScheduler.maximumRequestsPerServer = 3;

export const cesiumViewer = ref();

/* eslint-disable @typescript-eslint/camelcase */
// See also https://gitlab.kitware.com/smart/watch/-/blob/master/watch/heuristics.py#L45
// const HUERISTIC_STATUS_DATA = {
//   positive_annotated: '#808000', // olive
//   positive_partial: '#32CD32', // limegreen
//   positive_pending: '#2E8B57', // seagreen
//   positive_excluded: '#006400', // darkgreen
//   positive_unbounded: '#4682B4', // steelblue
//   negative: '#FF4500', // orangered
//   negative_unbounded: '#FF1493', // deeppink
//   ignore: '#800080', // purple
// };
const HUERISTIC_STATUS_DATA = {
  positive_annotated: '#000000',
  positive_partial: '#000000',
  positive_pending: '#000000',
  positive_excluded: '#006400',
  positive_unbounded: '#9400D3', // darkviolet
  negative: '#FF4500', // orangered
  negative_unbounded: '#FF1493', // deeppink
  ignore: '#FFA07A', // lightsalmon
};
/* eslint-enable @typescript-eslint/camelcase */

export const addGeojson = async (geojson: GeoJSON): Promise<GeoJsonDataSource> => {
  // cesiumViewer.value.dataSources.remove(source);
  const source = await cesiumViewer.value.dataSources.add(
    Cesium.GeoJsonDataSource.load(geojson),
  );
  // Change display properties for all entities in data source
  /* eslint-disable no-param-reassign */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  source.entities.values.forEach(async (entity: {polygon: any; properties: any}) => {
    let color;
    if (entity.properties?.status && entity.properties.status?._value in HUERISTIC_STATUS_DATA) {
      const status = entity.properties.status?._value as keyof typeof HUERISTIC_STATUS_DATA;
      const colorV = HUERISTIC_STATUS_DATA[status];
      color = Cesium.Color.fromCssColorString(colorV).withAlpha(0.25);
    } else {
      color = Cesium.Color.fromRandom().withAlpha(0.25);
    }
    entity.polygon.height = 0;
    entity.polygon.material = color;
    entity.polygon.outlineColor = Cesium.Color.BLACK;
    // entity.polygon.outline = true;
    // entity.polygon.outlineWidth = 30; // WebGL issue - doesn't do anything
  });
  /* eslint-enable no-param-reassign */

  return source;
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const getSelectedEntityFromPoint = (Position: any) => {
  const pickedObject = cesiumViewer.value.scene.pick(Position);
  // const pickedObjects = cesiumViewer.value.scene.drillPick(Position);
  // let picked = pickedObjects[0];

  if (!Cesium.defined(pickedObject)) {
    return null;
  }
  return pickedObject.id; // id -> Entity object
};
