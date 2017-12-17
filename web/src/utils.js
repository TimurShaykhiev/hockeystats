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
  }
};
