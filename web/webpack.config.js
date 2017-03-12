"use strict";

const path = require('path');

const DIST_DIR = path.resolve(__dirname, 'dist');
const SRC_DIR = path.resolve(__dirname, 'src');

const config = {
  entry:  SRC_DIR + '/main.js',
  output: {
    filename: 'bundle.js',
    path: DIST_DIR + "/app",
    publicPath: "/app/"
  },
  module: {
    loaders: [
      {
        test: /\.(js|jsx)$/,
        loader: 'babel-loader',
        include: SRC_DIR,
        query: {
          presets: ['es2015', 'react']
        }
      }
    ]
  },
  devServer: {
    contentBase: DIST_DIR + "/app",
    port: 9000
  }
};

module.exports = config;
