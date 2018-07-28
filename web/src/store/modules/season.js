import seasonApi from 'Api/season';
import {logger} from 'Root/logger';
import StoreUtils from 'Store/utils';
import UserSettings from 'Root/userSettings';

const settings = new UserSettings();

const state = {
  currentSeason: {},
  allSeasons: {},
  seasonStats: {},
  seasonInfo: {},
  selectedSeason: {},
  seasonPenalties: {}
};

const getters = {
  getSelectedSeason(state) {
    let season = state.selectedSeason;
    if (season.id === undefined) {
      season = settings.selectedSeason;
    }
    return season;
  },

  getSeasonInfo(state) {
    return (season) => {
      if (StoreUtils.isCorrectSeason(season, state.seasonInfo)) {
        return state.seasonInfo;
      }
      return null;
    };
  },

  getSeasonChartData(state) {
    return (chartName, season) => {
      let stats = state[chartName];
      if (StoreUtils.isCorrectSeason(season, stats)) {
        return stats;
      }
      return null;
    };
  }
};

function getDataBySeason(actName, mutName, stateName, commit, state, reqParams) {
  logger.debug(`action: ${actName}`);
  if (reqParams.isSeasonEqual(state[stateName].season)) {
    logger.debug(`action: ${actName} data is in storage`);
    return Promise.resolve(state[stateName]);
  }
  let requestPromise = seasonApi[actName](reqParams);
  return StoreUtils.processRequest(actName, mutName, stateName, commit, state, requestPromise);
}

function getDataForAllSeasons(actName, mutName, stateName, commit, state) {
  logger.debug(`action: ${actName}`);
  if (state[stateName].timestamp) {
    logger.debug(`action: ${actName} data is in storage`);
    return Promise.resolve(state[stateName]);
  }
  let requestPromise = seasonApi[actName]();
  return StoreUtils.processRequest(actName, mutName, stateName, commit, state, requestPromise);
}

const actions = {
  getCurrentSeason({commit, state}) {
    return getDataForAllSeasons('getCurrentSeason', 'setCurrentSeason', 'currentSeason', commit, state);
  },

  getAllSeasons({commit, state}) {
    return getDataForAllSeasons('getAllSeasons', 'setAllSeasons', 'allSeasons', commit, state);
  },

  getSeasonStats({commit, state}) {
    return getDataForAllSeasons('getSeasonStats', 'setSeasonStats', 'seasonStats', commit, state);
  },

  getSeasonInfo({commit, state}, {reqParams}) {
    return getDataBySeason('getSeasonInfo', 'setSeasonInfo', 'seasonInfo', commit, state, reqParams);
  },

  getSeasonPenalties({commit, state}, {reqParams}) {
    return getDataBySeason('getSeasonPenalties', 'setSeasonPenalties', 'seasonPenalties', commit, state, reqParams);
  }
};

function seasonStatsToObject(stats) {
  return {
    games: stats[0],
    goalsPerGame: stats[1],
    shotsPerGame: stats[2],
    pimPerGame: stats[3],
    blocksPerGame: stats[4],
    hitsPerGame: stats[5],
    ppPercentage: stats[6],
    regularWinPercentage: stats[7],
    overtimeWinPercentage: stats[8],
    shootoutWinPercentage: stats[9]
  };
}

const mutations = {
  setCurrentSeason(state, season) {
    logger.debug('mutation: setCurrentSeason');
    state.currentSeason = StoreUtils.convertSeason(season);
  },

  setAllSeasons(state, seasons) {
    logger.debug('mutation: setAllSeasons');
    state.allSeasons = seasons;
    state.allSeasons.seasons = state.allSeasons.seasons.map((s) => StoreUtils.convertSeason(s));
  },

  setSeasonStats(state, stats) {
    logger.debug('mutation: setSeasonStats');

    let processSeasonStats = (stats) => ({
      season: StoreUtils.convertSeason(stats.season),
      stats: seasonStatsToObject(stats.stats)
    });

    state.seasonStats = {
      regular: stats.regular.map((s) => processSeasonStats(s)),
      playoff: stats.po.map((s) => processSeasonStats(s))
    };
  },

  setSeasonInfo(state, stats) {
    logger.debug('mutation: setSeasonInfo');
    let info = {
      timestamp: stats.timestamp,
      season: StoreUtils.convertSeason(stats.season),
      stats: seasonStatsToObject(stats.stats),
      players: {},
      tops: {}
    };
    for (let p of stats.players) {
      info.players[p.id] = p;
    }
    for (let t of stats.tops) {
      info.tops[t.type] = {value: t.value, ids: t.ids};
    }
    state.seasonInfo = info;
  },

  setSelectedSeason(state, season) {
    logger.debug('mutation: setSelectedSeason');
    state.selectedSeason = season;
    settings.selectedSeason = season;
  },

  setSeasonPenalties(state, stats) {
    logger.debug('mutation: setSeasonPenalties');
    let season = StoreUtils.convertSeason(stats.season);
    state.seasonPenalties = {
      timestamp: stats.timestamp,
      season: season,
      data: stats.data
    };
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
