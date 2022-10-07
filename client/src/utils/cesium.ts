import * as Cesium from 'cesium';
import { buildModuleUrl, ProviderViewModel, UrlTemplateImageryProvider } from 'cesium';
import colormap from 'colormap';
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

function displayColorBar(tiles3dId: number, min: number, max: number, colorMap: number[][]) {
  const canvas = document.getElementById(`canvas-${tiles3dId}`) as HTMLCanvasElement;
  const ctx = canvas.getContext('2d') as CanvasRenderingContext2D;

  const gradient = ctx.createLinearGradient(0, 0, 300, 0);

  colorMap.forEach((colors: number[], i) => {
    // Convert color from array of three floats to `rgb(r,g,b)` format
    const color = `rgb(${colors.map((c: number) => c * 255).join(',')})`;
    gradient.addColorStop(i / 100, color);
  });

  // Set the fill style and draw a rectangle
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, 300, 30);
  ctx.font = '16px Roboto';

  ctx.fillStyle = '#000000';
  // Draw min and max values at opposite ends of the color bar
  ctx.fillText(parseFloat(min.toString()).toFixed(2), 0, 50);
  ctx.fillText(parseFloat(((max + min) / 2).toString()).toFixed(2), 265 / 2, 50);
  ctx.fillText(parseFloat(max.toString()).toFixed(2), 265, 50);
}

function hideColorBar(tiles3dId: number) {
  const canvas = document.getElementById(`canvas-${tiles3dId}`) as HTMLCanvasElement;
  const ctx = canvas.getContext('2d') as CanvasRenderingContext2D;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

export function createShader(
  tiles3dId: number,
  propertyName: string | undefined,
  sourceMin: number,
  sourceRange: number,
  colormapName?: string,
) {
  // Generate color map
  const colorMap: number[][] = colormap({
    colormap: colormapName,
    nshades: 101,
    format: 'float',
    alpha: 1,
  }).map((color: number[], i: number) => {
    if (i === 0) {
      return [0, 0, 0];
    }
    const newColor = JSON.parse(JSON.stringify(color));
    // remove the alpha value
    newColor.pop();
    return newColor;
  });

  // Lookup table for CE calculation
  const RLookupTable = [
    1.6449,
    1.6456,
    1.6479,
    1.6518,
    1.6573,
    1.6646,
    1.6738,
    1.6852,
    1.6992,
    1.7163,
    1.7371,
    1.7621,
    1.7915,
    1.8251,
    1.8625,
    1.9034,
    1.9472,
    1.9936,
    2.0424,
    2.0932,
    2.1460,
  ];

  hideColorBar(tiles3dId);

  // GLSL code for Cesium to generate shader
  let fragmentShaderText;

  if (propertyName === 'CE90') {
    fragmentShaderText = `
      vec2 eigenValues2x2(float m0_0, float m0_1, float m1_0, float m1_1)
      {
        // Calculates the eigenvalues of the given 2x2 matrix
        float p = m0_0 + m1_1;
        float q = m0_0 * m1_1 - m0_1 * m1_0;
        float r = sqrt(p * p - 4.0 * q);
        float vmax = 0.5 * (p + r);
        float vmin = 0.5 * (p - r);
        return vec2(vmax, vmin);
      }

      float R(float r)
      {
        float lookupTable[${RLookupTable.length}];
        ${RLookupTable.map((value, i) => `lookupTable[${i}] = ${value};`).join('\n')}
        int ndx = int(${RLookupTable.length - 1}.0 * r);
        for (int i = 0; i < ${RLookupTable.length}; i++) {
          if (i == ndx) {
            return lookupTable[i];
          }
        }
        return 0.0;
      }

      float CE(float m0_0, float m0_1, float m1_0, float m1_1)
      {
        vec2 eigenvalues = eigenValues2x2(m0_0, m0_1, m1_0, m1_1);

        float vmax = eigenvalues[0];
        float vmin = eigenvalues[1];

        float smax = sqrt(vmax);
        float smin = sqrt(vmin);

        float r = smin / smax;

        return R(r) * smax;
      }

      void fragmentMain(FragmentInput fsInput, inout czm_modelMaterial material)
      {
        // Generate colormap
        vec3 colormap[${colorMap.length}];
        ${colorMap.map((color: number[], i: number) => `colormap[${i}] = vec3(${color.join(',')})`).join(';\n')};

        // Min and max CE values
        float min = float(${sourceMin});
        float max = float(${sourceMin + sourceRange});

        // Actual CE value
        float ce = CE(fsInput.metadata.c0_0, fsInput.metadata.c1_0, fsInput.metadata.c1_0, fsInput.metadata.c1_1);

        if (ce > max) {
          ce = max;
        }

        // Normalize the CE value to a [0, 1] scale
        float normalized_0_1 = (ce - min) / (max - min);

        int colormapIndex = int(normalized_0_1 * 100.0);

        // The version of GLSL that Cesium uses doesn't support indexing arrays with variables.
        // But, the compiler will unroll constant-length loops, so we can use one here
        // to index the array with a variable.
        for (int i = 0; i < ${colorMap.length}; i++) {
          if (i == colormapIndex) {
            material.diffuse = colormap[i];
            return;
          }
        }

        // Make the shader return black to indicate failure if the index wasn't computed properly
        material.diffuse = vec3(0, 0, 0);
      }
    `;
  } else if (propertyName === 'LE90') {
    fragmentShaderText = `
      void fragmentMain(FragmentInput fsInput, inout czm_modelMaterial material)
      {
        // Generate colormap
        vec3 colormap[${colorMap.length}];
        ${colorMap.map((color: number[], i: number) => `colormap[${i}] = vec3(${color.join(',')})`).join(';\n')};

        float c2_2 = fsInput.metadata.c2_2;

        // Get minimum and maximum LE values
        float min = float(${sourceMin});
        float max = float(${sourceMin + sourceRange});

        // Compute actual LE value
        float LE = 1.6499 * sqrt(c2_2);

        if (LE > max) {
          LE = max;
        }

        // Normalize the LE value to a [0, 1] scale
        float normalized_0_1 = (LE - min) / (max - min);

        // Convert the normalized LE value into an index for the colormap array
        int colormapIndex = int(normalized_0_1 * 100.0);

        // The version of GLSL that Cesium uses doesn't support indexing arrays with variables.
        // But, the compiler will unroll constant-length loops, so we can use one here
        // to index the array with a variable.
        for (int i = 0; i < ${colorMap.length}; i++) {
            if (i == colormapIndex) {
              material.diffuse = colormap[i];
              return;
            }
        }

        // Make the shader return black to indicate failure if the index wasn't computed properly
        material.diffuse = vec3(0, 0, 0);
      }
    `;
  } else if (propertyName && /c\d_\d/.test(propertyName)) {
    fragmentShaderText = `
      void fragmentMain(FragmentInput fsInput, inout czm_modelMaterial material)
      {
        float value = float(fsInput.metadata.${propertyName});
        float range = ${sourceRange};
        float brightness = (value - float(${sourceMin})) / range;
        material.diffuse = vec3(brightness);
      }
    `;
  } else {
    // Otherwise, assume this is default and return undefined so that any existing custom
    // shaders are removed.
    return undefined;
  }

  displayColorBar(tiles3dId, sourceMin, sourceMin + sourceRange, colorMap);

  return new Cesium.CustomShader({ fragmentShaderText });
}

export function LE90(C2_2: number) {
  return 1.6499 * Math.sqrt(C2_2);
}

export function CE90(C0_0: number, C1_0: number, C1_1: number) {
  function eigenv2x2() {
    // char poly: x^2 - (a+d)x + (ad-bc) = 0
    const [a, b, c, d] = [C0_0, C1_0, C1_0, C1_1];
    const p = a + d;
    const q = a * d - b * c;
    const r = Math.sqrt(p * p - 4 * q);
    const vmax = 0.5 * (p + r);
    const vmin = 0.5 * (p - r);
    return [vmax, vmin];
  }
  function R(r: number) {
    const vals = [
      1.6449,
      1.6456,
      1.6479,
      1.6518,
      1.6573,
      1.6646,
      1.6738,
      1.6852,
      1.6992,
      1.7163,
      1.7371,
      1.7621,
      1.7915,
      1.8251,
      1.8625,
      1.9034,
      1.9472,
      1.9936,
      2.0424,
      2.0932,
      2.1460,
    ];
    const n = vals.length - 1;
    const ndx = Math.round(n * r);
    return vals[ndx];
  }
  const [vmax, vmin] = eigenv2x2();
  const smax = Math.sqrt(vmax);
  const smin = Math.sqrt(vmin);
  const r = smin / smax;
  return R(r) * smax;
}
