export function omitInteger(numStr) {
  let i = numStr.indexOf('.');
  return i !== -1 ? numStr.slice(i) : numStr;
}

export function toiToStr(timeOnIce) {
  let toi = Math.floor(timeOnIce);
  let min = Math.floor(toi / 60);
  let sec = toi % 60;
  return sec < 10 ? `${min}:0${sec}` : `${min}:${sec}`;
}

export function seasonToStr(season, translateFunc) {
  let years = `${season.year}-${season.year % 100 + 1}`;
  let str = season.regular ? 'season.regular' : 'season.playoff';
  return `${translateFunc(str)} ${years}`;
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

export function allStatsToChartData(allStats, fieldMap) {
  // Convert all seasons stats to chart data set.
  // Returns array of objects. The season is always in 'x' field. Play-offs are ignored.
  let result = [];
  for (let s of allStats) {
    if (!s.season.regular) {
      continue;
    }
    let obj = {};
    obj.x = `${s.season.year}-${s.season.year % 100 + 1}`;
    for (let m of fieldMap) {
      if (m.convert) {
        obj[m.to] = m.convert(s.stats[m.from]);
      } else {
        obj[m.to] = s.stats[m.from];
      }
    }
    result.push(obj);
  }
  return result;
}

export function seasonStatsToChartData(stats, axises, legendKey) {
  // Convert season stats to chart data set.
  return {
    legendKey: legendKey,
    data: axises.map((m) => ({key: m.key, value: stats[m.key]}))
  };
}
