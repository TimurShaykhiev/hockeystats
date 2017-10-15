import playersApi from 'Api/players';
import ApiErrors from 'Api/apiErrors';
import {logger} from 'Root/logger';

const state = {
  skaterStats: {},
  goalieStats: {}
};

const getters = {
};

function getPlayersSeasonStats(actName, mutName, stateName, commit, state, reqParams) {
  logger.debug(`action: ${actName}`);
  if (reqParams.isSeasonEqual(state[stateName].season)) {
    logger.debug(`action: ${actName} season is in storage`);
    return;
  }
  playersApi[actName](reqParams)
    .then(
      (result) => {
        logger.debug(`action: ${actName} result received`);
        commit(mutName, {stats: result});
      },
      (error) => {
        if (error.message === ApiErrors.DUPLICATE_REQUEST) {
          logger.debug(`action: ${actName} error: ${error.message}`);
        } else {
          logger.error(`action: ${actName} error: ${error.message}`);
        }
      }
    );
}

const actions = {
  getSkaterStats({commit, state}, {reqParams}) {
    getPlayersSeasonStats('getSkaterStats', 'setSkaterStats', 'skaterStats', commit, state, reqParams);
  },

  getGoalieStats({commit, state}, {reqParams}) {
    getPlayersSeasonStats('getGoalieStats', 'setGoalieStats', 'goalieStats', commit, state, reqParams);
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
  },

  setGoalieStats(state, {stats}) {
    logger.debug('mutation: setGoalieStats');
    let newStat = {};
    newStat.season = stats.season;
    newStat.goalies = [];
    for (let s of stats.results) {
      let goalie = {player: s.player, stats: {}};
      goalie.stats.toi = s.stats[0];
      goalie.stats.goals = s.stats[1];
      goalie.stats.assists = s.stats[2];
      newStat.goalies.push(goalie);
    }
    state.goalieStats = newStat;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
