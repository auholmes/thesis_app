const webpack = require('webpack');
const resolve = require('path').resolve;
const config = {
 devtool: 'eval-source-map',
 entry: __dirname + '/js/index.jsx',
 output:{
      path: resolve('.'),
      filename: 'bundle.js',
      publicPath: resolve('.')
},
 resolve: {
  extensions: ['.js','.jsx','.css']
 },
 module: {
  rules: [
  {
   test: /\.jsx?/,
   loader: 'babel-loader',
   exclude: /node_modules/,
  }]
 }
};
module.exports = config;
