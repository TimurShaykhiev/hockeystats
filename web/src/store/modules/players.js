import playersApi from 'Api/players';
import ApiErrors from 'Api/apiErrors';
import {logger} from 'Root/logger';

const state = {
  skaterStats: {}
};

const getters = {
};

const actions = {
  getSkatersStats({commit, state}, {reqParams}) {
    logger.debug('action: getSkaterStats');
    playersApi.getSkatersStats(reqParams)
      .then(
        (result) => {
          logger.debug('action: getSkaterStats result received');
          commit('setSkaterStats', {stats: result});
        },
        (error) => {
          if (error.message === ApiErrors.DUPLICATE_REQUEST) {
            logger.debug(`action: getSkaterStats error: ${error.message}`);
          } else {
            logger.error(`action: getSkaterStats error: ${error.message}`);
          }
        }
      );
  }
};

const mutations = {
  setSkaterStats(state, {stats}) {
    logger.debug('mutation: setSkaterStats');
    let newStat = {};
    newStat.season = stats.season;
    newStat.skaters = [];
    for (let s of stats.results) {
      let skater = {player: s.player, stats: {}};
      skater.stats.goals = s.stats[0];
      skater.stats.assists = s.stats[1];
      skater.stats.plusMinus = s.stats[2];
      skater.stats.toi = s.stats[3];
      newStat.skaters.push(skater);
    }
    state.skaterStats = newStat;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
