'use strict';

const path = require('path');
const webpack = require('webpack');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

const extractLess = new ExtractTextPlugin({
  filename: 'all.css',
  disable: process.env.NODE_ENV === 'development'
});

const DIST_DIR = path.resolve(__dirname, 'dist');
const SRC_DIR = path.resolve(__dirname, 'src');

const config = {
  entry: SRC_DIR + '/main.js',
  output: {
    filename: 'bundle.js',
    path: DIST_DIR + '/app',
    publicPath: '/app/'
  },
  module: {
    rules: [{
        test: /\.less$/,
        use: extractLess.extract({
          use: [{loader: 'css-loader'}, {loader: 'less-loader'}],
          // use style-loader in development
          fallback: 'style-loader'
        })
      }, {
        test: /\.vue$/,
        loader: 'vue-loader'
      }, {
        test: /\.js$/,
        loader: 'babel-loader',
        include: SRC_DIR
      }, {
        test: /\.(js|vue)$/,
        loader: 'eslint-loader',
        exclude: /node_modules/,
        options: {
          failOnWarning: false,
          failOnError: true
        }
      }
    ]
  },
  resolve: {
    extensions: ['.js', '.vue', '.json'],
    alias: {
      Components: SRC_DIR + '/components'
    }
  },
  plugins: [
    new CopyWebpackPlugin([{from: 'index.html'}]),
    extractLess
  ],
  devServer: {
    contentBase: DIST_DIR + '/app',
    port: 9000,
    host: '0.0.0.0'
  },
  devtool: '#eval-source-map'
};

module.exports = config;

if (process.env.NODE_ENV === 'production') {
  module.exports.devtool = '#source-map';
  module.exports.plugins = (module.exports.plugins || []).concat([
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"production"'
      }
    }),
    new webpack.optimize.UglifyJsPlugin({
      sourceMap: true,
      compress: {
        warnings: false
      }
    }),
    new webpack.LoaderOptionsPlugin({
      minimize: true
    })
  ]);
}
