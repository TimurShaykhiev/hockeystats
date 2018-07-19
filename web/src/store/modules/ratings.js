import ratingsApi from 'Api/ratings';
import {logger} from 'Root/logger';
import StoreUtils from 'Store/utils';

const state = {
  scorerDuos: {}
};

const getters = {
  getRating(state) {
    return (ratingName, season) => {
      let rating = state[ratingName];
      if (StoreUtils.isCorrectSeason(season, rating)) {
        return rating;
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
  let requestPromise = ratingsApi[actName](reqParams);
  return StoreUtils.processRequest(actName, mutName, stateName, commit, state, requestPromise);
}

const actions = {
  getScorerDuos({commit, state}, {reqParams}) {
    return getDataBySeason('getScorerDuos', 'setScorerDuos', 'scorerDuos', commit, state, reqParams);
  }
};

const mutations = {
  setScorerDuos(state, ratingData) {
    logger.debug('mutation: setScorerDuos');
    let season = StoreUtils.convertSeason(ratingData.season);
    state.scorerDuos = {
      timestamp: ratingData.timestamp,
      season: season,
      players: ratingData.players.reduce((map, el) => {
        map[el.id] = el;
        return map;
      }, {}),
      rating: ratingData.rating
    };
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
