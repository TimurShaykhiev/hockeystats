import {format} from 'd3-format';
import {NumValue, TimeValue} from 'Components/statValue';
import i18n from 'Root/locales';

function getPlayerName(s) {
  return s.player.name;
}

export default {
  omitInteger(num, precision) {
    let f = format(`.${precision}`);
    let numStr = f(num);
    if (num > 0 && num < 1) {
      // Omit integer part if it is 0
      return numStr.slice(1);
    }
    return numStr;
  },

  toiToStr(timeOnIce) {
    let toi = Math.floor(timeOnIce);
    let min = Math.floor(toi / 60);
    let sec = toi % 60;
    return sec < 10 ? `${min}:0${sec}` : `${min}:${sec}`;
  },

  seasonToStr(season) {
    let years = `${season.year}-${season.year % 100 + 1}`;
    let str = season.regular ? 'season.regular' : 'season.playoff';
    return `${i18n.t(str)} ${years}`;
  },

  getPaginationText() {
    return {
      next: i18n.t('pagination.next'),
      prev: i18n.t('pagination.prev'),
      rowsPerPage: i18n.t('pagination.rowsPerPage'),
      ofText: i18n.t('pagination.ofText'),
      allText: i18n.t('pagination.allText')
    };
  },

  allStatsToChartData(allStats, fieldMap) {
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
  },

  statsToChartData(stats, fieldMap, getNameFunc = getPlayerName) {
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
  },

  seasonStatsToChartData(stats, axises, legendKey, fieldMap) {
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
  },

  getAxis(statName, caption, getRangeFunc, currentSeason) {
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
  },

  filterName(str, filterStr) {
    return str.toLowerCase().indexOf(filterStr) !== -1;
  },

  getPlayerShortNames(d) {
    function shorten(str) {
      let tokens = str.split(' ');
      return tokens[tokens.length - 1].slice(0, 3).toUpperCase();
    }
    let name1 = shorten(d.player1.name);
    let name2 = shorten(d.player2.name);
    if (name1 === name2) {
      // If last names start with the same 3 characters, add first name character
      name1 = `${d.player1.name[0].toUpperCase()}.${name1}`;
      name2 = `${d.player2.name[0].toUpperCase()}.${name2}`;
    }
    return [name1, name2];
  },

  createMainStatCompare(data, attr, rateAttr, label, getNamesFunc, precision, order='desc') {
    let [lName, rName] = getNamesFunc(data);
    return {
      id: attr,
      label: label,
      leftData: {
        name: lName,
        value: new NumValue(data.stats1[attr], precision),
        rate: new NumValue(data.stats1[rateAttr])
      },
      rightData: {
        name: rName,
        value: new NumValue(data.stats2[attr], precision),
        rate: new NumValue(data.stats2[rateAttr])
      },
      sortOrder: order
    };
  },

  createStatCompare(data, title, getNamesFunc, fields) {
    let [lName, rName] = getNamesFunc(data);
    return {
      caption: {title: title, lName: lName, rName: rName},
      stats: fields.map((el) => ({
        name: el.name,
        lValue: el.time ? new TimeValue(data.stats1[el.attrName]) :
                          new NumValue(data.stats1[el.attrName], el.precision),
        rValue: el.time ? new TimeValue(data.stats2[el.attrName]) :
                          new NumValue(data.stats2[el.attrName], el.precision),
        sortOrder: el.order || 'desc'
      }))
    };
  }
};
