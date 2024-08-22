class Condition {
  constructor({ operator, left, right }) {
    this.operator = operator;
    this.left = left;
    this.right = right;
  }
}

module.exports = {
  Condition
};
