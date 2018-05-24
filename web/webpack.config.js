'use strict';

const path = require('path');
const fs = require('fs');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

const devBuild = process.env.NODE_ENV === 'development';
const deployBuild = process.env.NODE_ENV === 'deploy';

const extractLess = new ExtractTextPlugin({
  filename: devBuild ? 'all.css' : '[hash].css'
});

function getDistDirPath() {
  let base = path.resolve(__dirname, 'dist');
  if (deployBuild) {
    return base + '/deploy';
  }
  if (devBuild) {
    return base + '/dev';
  }
  return base + '/prod';
}

function getDevTool() {
  if (deployBuild) {
    return '';
  }
  if (devBuild) {
    return 'eval-source-map';
  }
  return 'source-map';
}

function makeDir(dirPath) {
  let exists = true;
  try {
    exists = fs.statSync(dirPath).isDirectory();
  } catch (e) {
    if (e.code === 'ENOENT') {
      exists = false;
    } else {
      throw e;
    }
  }
  if (!exists) {
    fs.mkdirSync(dirPath);
  }
}

const DIST_DIR = getDistDirPath();
const SRC_DIR = path.resolve(__dirname, 'src');
const ASSETS_DIR = path.resolve(__dirname, 'assets');
const CONFIG_DIR = path.resolve(__dirname, 'config');

const appConfigDev = require(CONFIG_DIR + '/devConfig.js');
const appConfigProduction = require(CONFIG_DIR + '/prodConfig.js');

makeDir(DIST_DIR);

const config = {
  entry: SRC_DIR + '/main.js',
  output: {
    filename: devBuild ? 'bundle.js' : '[hash].js',
    path: DIST_DIR
  },
  module: {
    rules: [{
        test: /\.css$/,
        use: extractLess.extract({
          use: ['css-loader']
        }),
        include: path.resolve(__dirname, 'node_modules')
      }, {
        test: /\.less$/,
        use: extractLess.extract({
          use: ['css-loader', 'postcss-loader', 'less-loader']
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
        include: SRC_DIR,
        options: {
          failOnWarning: false,
          failOnError: true
        }
      }, {
        test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
        loader: 'url-loader',
        options: {
          limit: 8192,
          name: '[name].[ext]',
          outputPath: 'images/'
        }
      }, {
        test: /\.(eot|svg|ttf|woff|woff2)$/,
        loader: 'file-loader',
        include: [ASSETS_DIR + '/fonts'],
        options: {
          name: '[name].[ext]',
          outputPath: 'fonts/'
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
      Store: SRC_DIR + '/store',
      ThirdParty: SRC_DIR + '/3rdparty',
      Assets: ASSETS_DIR
    }
  },
  plugins: [
    extractLess,
    new HtmlWebpackPlugin({
      template: 'index.template'
    }),
    new CopyWebpackPlugin([{from: ASSETS_DIR + '/images/team*.svg', to: 'images', flatten: true}]),
    new CopyWebpackPlugin([{from: ASSETS_DIR + '/favicons/*', to: '', flatten: true}]),
    new webpack.DefinePlugin({
      '__APP_CONFIG__': JSON.stringify(devBuild ? appConfigDev : appConfigProduction),
      'process.env': {
        NODE_ENV: devBuild ? '"development"' : '"production"'
      }
    })
  ],
  devServer: {
    contentBase: DIST_DIR,
    port: 9000,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        secure: false
      }
    }
  },
  devtool: getDevTool()
};

module.exports = config;
