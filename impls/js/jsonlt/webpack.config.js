const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    filename: 'jsonlt.js',
    path: path.resolve(__dirname, 'dist'),
    library: 'JSONLT',
    libraryTarget: 'umd',
    globalObject: 'this'
  },
  mode: 'production'
};
