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
  const dataSource = await Cesium.GeoJsonDataSource.load(geojson);
  dataSource.name = JSON.stringify(geojson); // save name that can be used to retrieve this later
  const source = await cesiumViewer.value.dataSources.add(dataSource);
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
    entity.properties = { ...entity.properties, name: JSON.stringify(geojson) };
  });
  /* eslint-enable no-param-reassign */

  return source;
};
