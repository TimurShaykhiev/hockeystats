import {format} from 'd3-format';

export function omitInteger(num, precision) {
  let f = format(`.${precision}`);
  let numStr = f(num);
  if (num > 0 && num < 1) {
    // Omit integer part if it is 0
    return numStr.slice(1);
  }
  return numStr;
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

function getPlayerName(s) {
  return s.player.name;
}

export function statsToChartData(stats, fieldMap, getNameFunc=getPlayerName) {
  // Convert stats to chart data set.
  // Returns array of objects. The name is always in 'x' field.
  let result = [];
  for (let s of stats) {
    let obj = {};
    let ignore = false;
    obj.x = getNameFunc(s);
    for (let m of fieldMap) {
      if (m.filterFn && !m.filterFn(s.stats[m.filterField])) {
        ignore = true;
        break;
      }
      if (m.convert) {
        obj[m.to] = m.convert(s.stats[m.from]);
      } else {
        obj[m.to] = s.stats[m.from];
      }
    }
    if (!ignore) {
      result.push(obj);
    }
  }
  return result;
}

export function seasonStatsToChartData(stats, axises, legendKey, fieldMap) {
  // Convert season stats to chart data set.
  let data;
  if (fieldMap) {
    data = axises.map((m) => ({key: m.key, value: stats[fieldMap[m.key]]}));
  } else {
    data = axises.map((m) => ({key: m.key, value: stats[m.key]}));
  }
  return {
    legendKey: legendKey,
    data: data
  };
}

export function getAxis(statName, caption, getRangeFunc, currentSeason) {
  if (getRangeFunc) {
    let range = getRangeFunc(statName);
    if (currentSeason && range[0] > 0) {
      // Ranges are calculated for completed season. While season is not finished the current stat value can be
      // less than min range. So set min range to 0 in order to have correct chart.
      range[0] = 0;
    }
    return {key: statName, name: caption, range: range};
  }
  return {key: statName, name: caption};
}

export function filterName(str, filterStr) {
  return str.toLowerCase().indexOf(filterStr) !== -1;
}
