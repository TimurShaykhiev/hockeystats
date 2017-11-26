export function floatToStr(number, precision, omitInteger=false) {
  // Convert to string with 'precision' digits after dot(aligned with trailing zeros)
  let factor = Math.pow(10, precision);
  number = Math.round(number * factor);
  let str = (number / factor).toString();
  let i = str.indexOf('.');
  if (i === -1) {
    if (omitInteger) {
      return str;
    }
    str += '.';
    i = str.length - 1;
  }
  str += '0000000000000000000';
  return str.slice(omitInteger ? i : 0, i + precision + 1);
}
