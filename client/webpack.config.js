// webpack.config.js

const path = require('path')
const webpack = require('webpack')

var envPlugin = new webpack.DefinePlugin({
  'process.env.NODE_ENV': `"${process.env.NODE_ENV}"`
})

if(process.env.NODE_ENV === 'production'){
  console.log('production mode');
  var plugins = [
    // new webpack.optimize.CommonsChunkPlugin('vendor', 'vendor.js','common.js'),
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.UglifyJsPlugin({
      compress: { warnings: false }
    }),
    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.optimize.LimitChunkCountPlugin({maxChunks: 15}),
    new webpack.optimize.MinChunkSizePlugin({minChunkSize: 10000}),
    new webpack.optimize.AggressiveMergingPlugin(),
    // new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /fr/),
    new webpack.IgnorePlugin(/^\.\/locale$/, /moment$/),
    envPlugin
  ]

  var devtool='cheap-module-source-map'

} else {
  var plugins = null,
    pluginsReact = ['react-hot-loader/babel'],
    devtool = 'eval'
}

let node_modules_dir = path.resolve(__dirname, 'node_modules');

module.exports = {
  devtool: devtool,
  entry: './src/app.js',
  output: {
    path: __dirname + '/../public /js',
    filename: 'bundle.js',
    publicPath: '/dist/'
  },
  module: {
    loaders: [ {
        test: /\.js$/,
        loaders: ['babel'],
        exclude: [node_modules_dir]
      },
      { test: /\.json$/, loader: 'json' },
      {
        test: /\.jsx?$/,
        include: path.join(__dirname, 'src'),
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react', 'stage-0']
        },
        plugins: pluginsReact,
        exclude: [node_modules_dir]
      },{
        test: /\.css$/,
        loader: 'style!css?modules'
      }
    ]
  },
  plugins: plugins,
  resolveLoader: {
    root: path.join(__dirname, 'node_modules')
  }
};
