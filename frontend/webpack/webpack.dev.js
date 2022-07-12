const { merge } = require('webpack-merge');
const common = require('./webpack.common');

module.exports = merge(common, {
  mode: 'development',
  entry: ['@babel/polyfill', './src/index.js'],
  // devtool: 'inline-source-map',
  devServer: {
    port: 3000,
    compress: true,
    // inline: true,
    // watchContentBase: true,
    historyApiFallback: true,
    disableHostCheck: true,
  },
});
