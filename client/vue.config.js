/* eslint-disable @typescript-eslint/no-var-requires */

const cesiumSource = 'node_modules/cesium/Source';
const cesiumWorkers = '../Build/Cesium/Workers';
const cesiumThirdParty = '../Build/Cesium/ThirdParty';
const cesiumAssets = '../Build/Cesium/Assets';
const cesiumWidgets = '../Build/Cesium/Widgets';
const path = require('path');
// eslint-disable-next-line import/no-extraneous-dependencies
const webpack = require('webpack');
// eslint-disable-next-line import/no-extraneous-dependencies
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
  lintOnSave: false,

  configureWebpack: {
    plugins: [
      // Copy Cesium Assets, Widgets, and Workers to a static directory
      new CopyWebpackPlugin([{ from: path.join(cesiumSource, cesiumWorkers), to: 'Workers' }]),
      new CopyWebpackPlugin([{ from: path.join(cesiumSource, cesiumAssets), to: 'Assets' }]),
      new CopyWebpackPlugin([{ from: path.join(cesiumSource, cesiumWidgets), to: 'Widgets' }]),
      new CopyWebpackPlugin([{ from: path.join(cesiumSource, cesiumThirdParty), to: 'ThirdParty' }]),
      // Define relative base path in cesium for loading assets
      new webpack.DefinePlugin({ CESIUM_BASE_URL: JSON.stringify('') }),
    ],
    module: {
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
