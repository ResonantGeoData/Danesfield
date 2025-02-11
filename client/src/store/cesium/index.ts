import { Color, GeoJsonDataSource, RequestScheduler } from 'cesium';
import { ref } from 'vue';
import type { GeoJSON } from 'geojson';  // eslint-disable-line

// Don't limit the amount of requests Cesium can make at once
RequestScheduler.throttleRequests = false;

export const cesiumViewer = ref();

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

export const addGeojson = async (geojson: GeoJSON, key: string): Promise<GeoJsonDataSource> => {
  const dataSource = await GeoJsonDataSource.load(geojson);
  dataSource.name = key; // save name that can be used to retrieve this later
  const source = await cesiumViewer.value.dataSources.add(dataSource);
  // Change display properties for all entities in data source
  /* eslint-disable no-param-reassign */
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  source.entities.values.forEach(async (entity: {polygon: any; properties: any}) => {
    let color;
    // eslint-disable-next-line no-underscore-dangle
    if (entity.properties?.status && entity.properties.status?._value in HUERISTIC_STATUS_DATA) {
      // eslint-disable-next-line no-underscore-dangle
      const status = entity.properties.status?._value as keyof typeof HUERISTIC_STATUS_DATA;
      const colorV = HUERISTIC_STATUS_DATA[status];
      color = Color.fromCssColorString(colorV).withAlpha(0.25);
    } else {
      color = Color.fromRandom().withAlpha(0.25);
    }
    entity.polygon.height = 0;
    entity.polygon.material = color;
    entity.polygon.outlineColor = Color.BLACK;
    entity.properties = { ...entity.properties, name: JSON.stringify(geojson) };
  });
  /* eslint-enable no-param-reassign */

  return source;
};
