export function floatToStr(number, precision, omitInteger=false) {
  let factor = Math.pow(10, precision);
  number = Math.floor(number * factor);
  let str = (number / factor).toString();
  if (omitInteger) {
    let i = str.indexOf('.');
    return (i !== -1) ? str.slice(i) : str;
  }
  return str;
}
