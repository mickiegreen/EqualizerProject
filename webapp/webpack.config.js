'use strict';

const path = require('path');
const webpack = require('webpack');
const autoprefixer = require('autoprefixer');
const precss = require('precss');
const BundleTracker = require('webpack-bundle-tracker');
const ExtractTextPlugin = require("extract-text-webpack-plugin");
const dotenv = require('dotenv');

dotenv.load();
let appEntry;
let devtool;
let plugins;
let publicPath;



const stats = new BundleTracker(
    {
        path: __dirname,
        filename: 'static/webpack-stats.json',
        indent: true
    });

const env = process.env;
//const devServerPort = env.WEBPACK_PORT ? env.WEBPACK_PORT : 40743;
const devServerPort = 40743;
//const staticResourcesPort = 8000;

const staticResourcesPort = 40743;

if (process.env.NODE_ENV === 'production') {
    appEntry = [path.join(__dirname, 'client/index.js')];
    devtool = 'source-map';
    publicPath = '/assets/bundles/';
    plugins = [
        stats,
        new webpack.optimize.OccurrenceOrderPlugin(),
        new webpack.optimize.CommonsChunkPlugin({name: 'vendor', filename: 'vendor.js'}),
        new webpack.DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify('production')
            }
        }),
        new ExtractTextPlugin({
            filename: '[name]-[hash].css',
            allChunks: true
          }
        ),
        new webpack.optimize.UglifyJsPlugin({
            compress: {
                warnings: false
            }
        }),
    ];
} else {
    appEntry = [
    // activate HMR for React
    'react-hot-loader/patch',
    `webpack-dev-server/client?http://localhost:${devServerPort}`,
    'webpack/hot/only-dev-server',
    './client/index.js'
    ];
    publicPath = `http://localhost:${devServerPort}/assets/bundles/`; // Tell django to use this URL to load packages and not use STATIC_URL + bundle_name
    devtool = 'eval';
    plugins = [
        stats,
        new webpack.optimize.CommonsChunkPlugin({name: 'vendor', filename: 'vendor.js'}),
        new ExtractTextPlugin({
                filename: '[name]-[hash].css',
                allChunks: true
              }
        ),
        new webpack.NoEmitOnErrorsPlugin(),
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NamedModulesPlugin(),
        new webpack.DefinePlugin({
            __DEV__: true
        }),
    ];
}

const buildPath = path.join(__dirname, 'static', 'bundles');


module.exports = {
  entry: {
    app: appEntry,
    vendor: ['react', 'react-dom', 'react-relay', 'react-router']
  },
  output: {
    path: buildPath,
    filename: "[name]-[hash].js",
    publicPath: publicPath
  },
  devtool,
  devServer: {
    hot: true,
    port: devServerPort,
    historyApiFallback: true,
    stats: "errors-only",
    contentBase: buildPath,
    headers: {
      "Access-Control-Allow-Origin": "*"
    },
    publicPath
  },
  module: {

        rules: [{
            test: /\.jsx?$/,
            use: 'babel-loader',
            exclude: /node_modules/
        }, {
      test: /\.css$/,
      use: ExtractTextPlugin.extract({
        fallback: "style-loader",
        use: {
          loader: 'css-loader',
          options: {

          }
        }
      })
    }, {
      test: /\.scss$/,
      include: [path.join(__dirname, 'node_modules'), path.join(__dirname, 'client', 'styles')],
      use: ExtractTextPlugin.extract({
        fallback: "style-loader",
        use: [
          'css-loader',
          {
            loader: 'sass-loader',
            options: {
              includePaths: [
                path.resolve(__dirname, 'node_modules'),
                path.join(__dirname, 'client', 'styles')
              ],
            }
          },
        ]
      })
    },
      {
        test: /\.scss$/,
        exclude: [path.join(__dirname, 'node_modules'), path.join(__dirname, 'client', 'styles')],
        include: path.join(__dirname, 'client'),
        use: ExtractTextPlugin.extract({
          fallback: "style-loader",
          use: [{
            loader: 'css-loader',
            options: {
              modules: true
            }},
            {
              loader: 'sass-loader',
              options: {
                includePaths: [
                  path.resolve(__dirname, 'node_modules'),
                  path.join(__dirname, 'client', 'styles')
                ],
              }
            },
          ]
        })
      }, {
        test: /\.(png|jpg|jpeg|gif|svg|woff|woff2)$/,
        use: [
          {
            loader: 'url-loader',
            options: {
              limit: 1000,
              name: "assets/[hash].[ext]"
            }
          }
        ]
      },
            { test: /\.(png|woff|woff2|eot|ttf|svg)$/, loader: 'url-loader?limit=100000' }
            ]
  },
  resolve: {
    alias: {
      components: path.resolve(__dirname, 'client/components'),
      modules: path.resolve(__dirname, 'client/modules'),
    }
  },
  plugins
};
