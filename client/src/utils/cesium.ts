import * as Cesium from 'cesium';
import { buildModuleUrl, ProviderViewModel, UrlTemplateImageryProvider } from 'cesium';
import { cesiumViewer } from '@/store/cesium';

/* Stamen's website (http://maps.stamen.com) as of 2019-08-28 says that the
 * maps they host may be used free of charge.  For http access, use a url like
 * http://{s}.tile.stamen.com/toner-lite/{z}/{x}/{y}.png */
export const StamenAttribution = 'Map tiles by <a href="http://stamen.com">Stamen '
       + 'Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">'
       + 'CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap'
       + '</a>, under <a href="http://www.openstreetmap.org/copyright">ODbL</a>.';

/* Per Carto's website regarding basemap attribution: https://carto.com/help/working-with-data/attribution/#basemaps */
export const CartoAttribution = 'Map tiles by <a href="https://carto.com">Carto</a>, under CC BY 3.0. Data by <a href="https://www.openstreetmap.org/">OpenStreetMap</a>, under ODbL.';

// Create ProviderViewModel based on different imagery sources
// - these can be used without Cesium Ion
export const imageryViewModels = [
  new ProviderViewModel({
    name: 'OpenStreetMap',
    iconUrl: buildModuleUrl('Widgets/Images/ImageryProviders/openStreetMap.png'),
    tooltip: 'OpenStreetMap (OSM) is a collaborative project to create a free editable map of the world.\nhttp://www.openstreetmap.org',
    creationFunction() {
      return new UrlTemplateImageryProvider({
        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        subdomains: 'abc',
        minimumLevel: 0,
        maximumLevel: 19,
      });
    },
  }),
  new ProviderViewModel({
    name: 'Positron',
    tooltip: 'CartoDB Positron basemap',
    iconUrl: 'http://a.basemaps.cartocdn.com/light_all/5/15/12.png',
    creationFunction() {
      return new UrlTemplateImageryProvider({
        url: 'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
        credit: CartoAttribution,
        minimumLevel: 0,
        maximumLevel: 18,
      });
    },
  }),
  new ProviderViewModel({
    name: 'Positron without labels',
    tooltip: 'CartoDB Positron without labels basemap',
    iconUrl: 'http://a.basemaps.cartocdn.com/rastertiles/light_nolabels/5/15/12.png',
    creationFunction() {
      return new UrlTemplateImageryProvider({
        url: 'https://{s}.basemaps.cartocdn.com/rastertiles/light_nolabels/{z}/{x}/{y}.png',
        credit: CartoAttribution,
        minimumLevel: 0,
        maximumLevel: 18,
      });
    },
  }),
  new ProviderViewModel({
    name: 'Dark Matter',
    tooltip: 'CartoDB Dark Matter basemap',
    iconUrl: 'http://a.basemaps.cartocdn.com/rastertiles/dark_all/5/15/12.png',
    creationFunction() {
      return new UrlTemplateImageryProvider({
        url: 'https://{s}.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}.png',
        credit: CartoAttribution,
        minimumLevel: 0,
        maximumLevel: 18,
      });
    },
  }),
  new ProviderViewModel({
    name: 'Dark Matter without labels',
    tooltip: 'CartoDB Dark Matter without labels basemap',
    iconUrl: 'http://a.basemaps.cartocdn.com/rastertiles/dark_nolabels/5/15/12.png',
    creationFunction() {
      return new UrlTemplateImageryProvider({
        url: 'https://{s}.basemaps.cartocdn.com/rastertiles/dark_nolabels/{z}/{x}/{y}.png',
        credit: CartoAttribution,
        minimumLevel: 0,
        maximumLevel: 18,
      });
    },
  }),
  new ProviderViewModel({
    name: 'Voyager',
    tooltip: 'CartoDB Voyager basemap',
    iconUrl: 'http://a.basemaps.cartocdn.com/rastertiles/voyager_labels_under/5/15/12.png',
    creationFunction() {
      return new UrlTemplateImageryProvider({
        url: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}.png',
        credit: CartoAttribution,
        minimumLevel: 0,
        maximumLevel: 18,
      });
    },
  }),
  new ProviderViewModel({
    name: 'Voyager without labels',
    tooltip: 'CartoDB Voyager without labels basemap',
    iconUrl: 'http://a.basemaps.cartocdn.com/rastertiles/voyager_nolabels/5/15/12.png',
    creationFunction() {
      return new UrlTemplateImageryProvider({
        url: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager_nolabels/{z}/{x}/{y}.png',
        credit: CartoAttribution,
        minimumLevel: 0,
        maximumLevel: 18,
      });
    },
  }),
  new ProviderViewModel({
    name: 'National Map Satellite',
    tooltip: 'National Map Satellite',
    iconUrl: 'https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/4/6/4',
    creationFunction() {
      return new UrlTemplateImageryProvider({
        url: 'https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}',
        credit: 'Tile data from <a href="https://basemap.nationalmap.gov/">USGS</a>',
        minimumLevel: 0,
        maximumLevel: 16,
      });
    },
  }),
  new ProviderViewModel({
    name: 'Stamen Terrain',
    tooltip: 'Stamen Terrain',
    iconUrl: 'https://stamen-tiles-a.a.ssl.fastly.net/terrain/5/15/12.png',
    creationFunction() {
      return new UrlTemplateImageryProvider({
        url: 'https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png',
        credit: StamenAttribution,
        subdomains: 'abcd',
        minimumLevel: 0,
        maximumLevel: 14,
      });
    },
  }),
  new ProviderViewModel({
    name: 'Stamen Terrain Background',
    tooltip: 'Stamen Terrain Background',
    iconUrl: 'https://stamen-tiles-a.a.ssl.fastly.net/terrain-background/5/15/12.png',
    creationFunction() {
      return new UrlTemplateImageryProvider({
        url: 'https://stamen-tiles-{s}.a.ssl.fastly.net/terrain-background/{z}/{x}/{y}.png',
        credit: StamenAttribution,
        subdomains: 'abcd',
        minimumLevel: 0,
        maximumLevel: 14,
      });
    },
  }),
  new ProviderViewModel({
    name: 'Stamen Toner',
    tooltip: 'Stamen Toner',
    iconUrl: 'https://stamen-tiles-a.a.ssl.fastly.net/toner/5/15/12.png',
    creationFunction() {
      return new UrlTemplateImageryProvider({
        url: 'https://stamen-tiles-{s}.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
        credit: StamenAttribution,
        subdomains: 'abcd',
        minimumLevel: 0,
        maximumLevel: 14,
      });
    },
  }),
  new ProviderViewModel({
    name: 'Stamen Toner Lite',
    tooltip: 'Stamen Toner',
    iconUrl: 'https://stamen-tiles-a.a.ssl.fastly.net/toner-lite/5/15/12.png',
    creationFunction() {
      return new UrlTemplateImageryProvider({
        url: 'https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.png',
        credit: StamenAttribution,
        subdomains: 'abcd',
        minimumLevel: 0,
        maximumLevel: 14,
      });
    },
  }),
];

export function renderFlightPath(id: number, flightData: number[][]): Cesium.Entity {
  // ref: https://cesium.com/learn/cesiumjs-learn/cesiumjs-flight-tracker/
  const timeStepInSeconds = 30;
  const totalSeconds = timeStepInSeconds * (flightData.length - 1);
  const start = Cesium.JulianDate.fromIso8601('2020-03-09T23:10:00Z');
  const stop = Cesium.JulianDate.addSeconds(start, totalSeconds, new Cesium.JulianDate());
  cesiumViewer.value.clock.startTime = start.clone();
  cesiumViewer.value.clock.stopTime = stop.clone();
  cesiumViewer.value.clock.currentTime = start.clone();
  cesiumViewer.value.timeline.zoomTo(start, stop);
  // Speed up the playback speed 50x.
  cesiumViewer.value.clock.multiplier = 50;
  // Start playing the scene.
  cesiumViewer.value.clock.shouldAnimate = true;

  // The SampledPositionedProperty stores the position and timestamp for each
  // sample along the radar sample series.
  const positionProperty = new Cesium.SampledPositionProperty();

  for (let i = 0; i < flightData.length; i += 1) {
    const dataPoint = flightData[i];

    // Declare the time for this individual sample
    // and store it in a new JulianDate instance.
    const time = Cesium.JulianDate.addSeconds(
      start, i * timeStepInSeconds, new Cesium.JulianDate(),
    );
    const position = Cesium.Cartesian3.fromDegrees(dataPoint[0], dataPoint[1]);

    // Store the position along with its timestamp.
    // Here we add the positions all upfront, but these can be added at run-time as
    // samples are received from a server.
    positionProperty.addSample(time, position);

    cesiumViewer.value.entities.add({
      id: `flight_path_${id}_point_${position.x}_${position.y}_${position.z}`,
      description: `Location: (${position.x}, ${position.y}, ${position.z})`,
      position,
      point: { pixelSize: 10, color: Cesium.Color.RED },
    });
  }
  // Create an entity to both visualize the entire radar sample series with a
  // line and add a point that moves along the samples.
  const airplaneEntity = cesiumViewer.value.entities.add({
    id: `flight_path_${id}_airplane`,
    availability: new Cesium.TimeIntervalCollection([new Cesium.TimeInterval({ start, stop })]),
    position: positionProperty,
    point: { pixelSize: 30, color: Cesium.Color.GREEN },
    path: new Cesium.PathGraphics({ width: 3 }),
  });

  cesiumViewer.value.flyTo(airplaneEntity, {
    offset: new Cesium.HeadingPitchRange(
      Cesium.Math.toRadians(0),
      Cesium.Math.toRadians(-90.0),
    ),
  });

  return airplaneEntity;
}
