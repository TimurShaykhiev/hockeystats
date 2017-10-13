'use strict';

const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

const devBuild = process.env.NODE_ENV === 'development';

const extractLess = new ExtractTextPlugin({
  filename: devBuild ? 'all.css' : '[hash].css'
});

const DIST_DIR = path.resolve(__dirname, 'dist');
const SRC_DIR = path.resolve(__dirname, 'src');

const config = {
  entry: SRC_DIR + '/main.js',
  output: {
    filename: devBuild ? 'bundle.js' : '[hash].js',
    path: DIST_DIR
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
      Root: SRC_DIR,
      Components: SRC_DIR + '/components',
      Api: SRC_DIR + '/api',
      Store: SRC_DIR + '/store'
    }
  },
  plugins: [
    new CopyWebpackPlugin([{from: 'assets'}]),
    extractLess,
    new HtmlWebpackPlugin({
      template: 'index.template'
    })
  ],
  devServer: {
    contentBase: DIST_DIR,
    port: 9000,
    host: '0.0.0.0'
  },
  devtool: devBuild ? 'eval-source-map' : 'source-map'
};

module.exports = config;
