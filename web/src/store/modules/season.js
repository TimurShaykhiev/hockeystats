import seasonApi from 'Api/season';
import {logger} from 'Root/logger';
import {commitNew} from 'Store/utils';

const state = {
  currentSeason: {}
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
          commitNew(commit, 'setCurrentSeason', state.currentSeason, result);
          return state.currentSeason;
        },
        (error) => {
          logger.error(`action: getCurrentSeason error: ${error.message}`);
        }
      );
  }
};

const mutations = {
  setCurrentSeason(state, season) {
    logger.debug('mutation: setCurrentSeason');
    state.currentSeason = season;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};