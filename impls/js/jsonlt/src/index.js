const { jsonltTransform } = require('./xform');

module.exports = {
  transform: jsonltTransform
};

// For browser usage
if (typeof window !== 'undefined') {
  window.JSONLT = { transform: jsonltTransform };
}
