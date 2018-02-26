export default {
  sortBy(arr, elemFunc, descOrder=false) {
    return arr.sort((a, b) => {
      let value1 = elemFunc(a);
      let value2 = elemFunc(b);
      if (value1 < value2) {
        return descOrder ? 1 : -1;
      }
      if (value1 > value2) {
        return descOrder ? -1 : 1;
      }
      return 0;
    });
  },

  percentile(array, p) {
    array.sort((a, b) => a - b);
    let len = array.length - 1;
    let index = p / 100. * len;
    let i = Math.floor(index);
    if (i >= len) {
      return array[len];
    }
    return array[i] + (array[i + 1] - array[i]) * (index - i);
  }
};
