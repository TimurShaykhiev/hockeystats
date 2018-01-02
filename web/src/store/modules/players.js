import playersApi from 'Api/players';
import {logger} from 'Root/logger';
import {commitNew} from 'Store/utils';

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
    return Promise.resolve(state[stateName]);
  }
  return playersApi[actName](reqParams)
    .then(
      (result) => {
        logger.debug(`action: ${actName} result received`);
        commitNew(commit, mutName, state[stateName], result);
        return state[stateName];
      },
      (error) => {
        logger.error(`action: ${actName} error: ${error.message}`);
      }
    );
}

const actions = {
  getSkaterStats({commit, state}, {reqParams}) {
    return getPlayersSeasonStats('getSkaterStats', 'setSkaterStats', 'skaterStats', commit, state, reqParams);
  },

  getGoalieStats({commit, state}, {reqParams}) {
    return getPlayersSeasonStats('getGoalieStats', 'setGoalieStats', 'goalieStats', commit, state, reqParams);
  }
};

const mutations = {
  setSkaterStats(state, stats) {
    logger.debug('mutation: setSkaterStats');
    let newStat = {};
    newStat.timestamp = stats.timestamp;
    newStat.season = stats.season;
    newStat.skaters = [];
    for (let s of stats.results) {
      let skater = {player: s.player, stats: {}};
      skater.stats.assists = s.stats[0];
      skater.stats.goals = s.stats[1];
      skater.stats.shots = s.stats[2];
      skater.stats.ppGoals = s.stats[3];
      skater.stats.penaltyMinutes = s.stats[4];
      skater.stats.shGoals = s.stats[5];
      skater.stats.plusMinus = s.stats[6];
      skater.stats.games = s.stats[7];
      skater.stats.points = s.stats[8];
      skater.stats.ppPoints = s.stats[9];
      skater.stats.shPoints = s.stats[10];
      skater.stats.pointsPerGame = s.stats[11];
      skater.stats.toiPerGame = s.stats[12];
      skater.stats.shootingPercentage = s.stats[13];
      skater.stats.faceOffWinsPercentage = s.stats[14];

      newStat.skaters.push(skater);
    }
    state.skaterStats = newStat;
  },

  setGoalieStats(state, stats) {
    logger.debug('mutation: setGoalieStats');
    let newStat = {};
    newStat.timestamp = stats.timestamp;
    newStat.season = stats.season;
    newStat.goalies = [];
    for (let s of stats.results) {
      let goalie = {player: s.player, stats: {}};
      goalie.stats.toi = s.stats[0];
      goalie.stats.assists = s.stats[1];
      goalie.stats.goals = s.stats[2];
      goalie.stats.penaltyMinutes = s.stats[3];
      goalie.stats.shots = s.stats[4];
      goalie.stats.saves = s.stats[5];
      goalie.stats.games = s.stats[6];
      goalie.stats.wins = s.stats[7];
      goalie.stats.shutout = s.stats[8];
      goalie.stats.points = s.stats[9];
      goalie.stats.losses = s.stats[10];
      goalie.stats.goalsAgainst = s.stats[11];
      goalie.stats.gaa = s.stats[12];
      goalie.stats.svp = s.stats[13];

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
