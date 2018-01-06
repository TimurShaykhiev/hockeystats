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

export function toiToStr(timeOnIce) {
  let toi = Math.floor(timeOnIce);
  let min = Math.floor(toi / 60);
  let sec = toi % 60;
  return sec < 10 ? `${min}:0${sec}` : `${min}:${sec}`;
}

export function getSeasonName(selectedSeason, seasons, translateFunc) {
  for (let s of seasons) {
    if (s.id === selectedSeason.id) {
      let years = `${s.year}-${s.year % 100 + 1}`;
      let str = selectedSeason.regular ? 'season.regular' : 'season.playoff';
      return `${translateFunc(str)} ${years}`;
    }
  }
  return '';
}

export function getPaginationText(translateFunc) {
  return {
    next: translateFunc('pagination.next'),
    prev: translateFunc('pagination.prev'),
    rowsPerPage: translateFunc('pagination.rowsPerPage'),
    ofText: translateFunc('pagination.ofText'),
    allText: translateFunc('pagination.allText')
  };
}

export function numberToOrdinal(num, translateFunc) {
  // Now it is applicable for english and russian languages only
  let rem = num % 100;
  if (rem === 11 || rem === 12 || rem === 12) {
    return `${num}${translateFunc('ordinalNumbers[0]')}`;
  }
  return `${num}${translateFunc(`ordinalNumbers[${num % 10}]`)}`;
}
