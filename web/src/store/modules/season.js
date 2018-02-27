import seasonApi from 'Api/season';
import {logger} from 'Root/logger';
import StoreUtils from 'Store/utils';

const state = {
  currentSeason: {},
  allSeasons: {},
  selectedSeason: {}
};

const getters = {
};

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
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
