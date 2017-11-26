import playersApi from 'Api/players';
import {logger} from 'Root/logger';
import {commitNew, getPercentage} from 'Store/utils';

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
      skater.stats.hits = s.stats[3];
      skater.stats.ppGoals = s.stats[4];
      skater.stats.ppAssists = s.stats[5];
      skater.stats.penaltyMinutes = s.stats[6];
      skater.stats.faceOffWins = s.stats[7];
      skater.stats.faceOffTaken = s.stats[8];
      skater.stats.takeaways = s.stats[9];
      skater.stats.giveaways = s.stats[10];
      skater.stats.shGoals = s.stats[11];
      skater.stats.shAssists = s.stats[12];
      skater.stats.blocked = s.stats[13];
      skater.stats.plusMinus = s.stats[14];
      skater.stats.toi = s.stats[15];
      skater.stats.evenToi = s.stats[16];
      skater.stats.ppToi = s.stats[17];
      skater.stats.shToi = s.stats[18];
      skater.stats.games = s.stats[19];
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
      goalie.stats.ppSaves = s.stats[6];
      goalie.stats.shSaves = s.stats[7];
      goalie.stats.evenSaves = s.stats[8];
      goalie.stats.shShotsAgainst = s.stats[9];
      goalie.stats.evenShotsAgainst = s.stats[10];
      goalie.stats.ppShotsAgainst = s.stats[11];
      goalie.stats.games = s.stats[12];
      goalie.stats.wins = s.stats[13];
      goalie.stats.shutout = s.stats[14];
      // Calculate some stats
      goalie.stats.gaa = getGoalsAgainstAverage(goalie.stats);
      goalie.stats.svp = getPercentage(goalie.stats.saves, goalie.stats.shots, true);

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

function getGoalsAgainstAverage(stats) {
  if (stats.toi > 0) {
    return (stats.shots - stats.saves) * 60 / Math.round(stats.toi / 60);
  }
  return 0;
}
