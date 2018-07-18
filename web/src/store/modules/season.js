import seasonApi from 'Api/season';
import {logger} from 'Root/logger';
import StoreUtils from 'Store/utils';
import UserSettings from 'Root/userSettings';

const settings = new UserSettings();

const state = {
  currentSeason: {},
  allSeasons: {},
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

const actions = {
  getCurrentSeason({commit, state}) {
    logger.debug('action: getCurrentSeason');
    if (state.currentSeason.timestamp) {
      logger.debug('action: getCurrentSeason current season is in storage');
      return Promise.resolve(state.currentSeason);
    }
    return seasonApi.getCurrentSeason()
      .then(
        (result) => {
          logger.debug('action: getCurrentSeason result received');
          StoreUtils.commitNew(commit, 'setCurrentSeason', state.currentSeason, result);
          return state.currentSeason;
        },
        (error) => {
          logger.error(`action: getCurrentSeason error: ${error.message}`);
        }
      );
  },

  getAllSeasons({commit, state}) {
    logger.debug('action: getAllSeasons');
    if (state.allSeasons.timestamp) {
      logger.debug('action: getAllSeasons seasons are in storage');
      return Promise.resolve(state.allSeasons);
    }
    return seasonApi.getAllSeasons()
      .then(
        (result) => {
          logger.debug('action: getAllSeasons result received');
          StoreUtils.commitNew(commit, 'setAllSeasons', state.allSeasons, result);
          return state.allSeasons;
        },
        (error) => {
          logger.error(`action: getAllSeasons error: ${error.message}`);
        }
      );
  },

  getSeasonPenalties({commit, state}, {reqParams}) {
    return getDataBySeason('getSeasonPenalties', 'setSeasonPenalties', 'seasonPenalties', commit, state, reqParams);
  }
};

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
