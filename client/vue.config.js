/* eslint-disable @typescript-eslint/no-var-requires */

const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');
// eslint-disable-next-line import/no-extraneous-dependencies
const webpack = require('webpack');

const cesiumSource = 'node_modules/cesium/Source/';
const cesiumBuild = 'node_modules/cesium/Build/Cesium/';

module.exports = {
  lintOnSave: false,

  configureWebpack: {
    resolve: {
      alias: {
        cesium: path.resolve(__dirname, './node_modules/cesium/Source'),
      },
    },
    plugins: [
      new CopyWebpackPlugin({
        patterns: [
          { from: `${cesiumBuild}Workers`, to: 'Workers' },
          { from: `${cesiumBuild}ThirdParty`, to: 'ThirdParty' },
          { from: `${cesiumBuild}Assets`, to: 'Assets' },
          { from: `${cesiumBuild}Widgets`, to: 'Widgets' },
        ],
      }),
      new webpack.DefinePlugin({
        // Define relative base path in cesium for loading assets
        CESIUM_BASE_URL: JSON.stringify('./'),
      }),
    ],
    module: {
      unknownContextRegExp: /\/cesium\/cesium\/Source\/Core\/buildModuleUrl\.js/,
      unknownContextCritical: false,
      rules: [{
        // Remove pragmas within cesium as recommended - https://github.com/AnalyticalGraphicsInc/cesium-webpack-example/blob/master/webpack.release.config.js
        test: /\.js$/,
        enforce: 'pre',
        include: path.resolve(__dirname, cesiumSource),
        sideEffects: false,
        use: [{
          loader: 'strip-pragma-loader',
          options: {
            pragmas: {
              debug: false,
            },
          },
        }],
      }, {
        test: /\.js$/,
        include: path.resolve(__dirname, cesiumSource),
        use: { loader: require.resolve('@open-wc/webpack-import-meta-loader') },
      },
      ],
    },
  },

  transpileDependencies: [
    // If babel ends up being required, this line is necessary. Without it,
    //  it has no effect.
    'vuetify',
  ],
};
