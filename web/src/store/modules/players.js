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
      skater.stats.hits = s.stats[3];
      skater.stats.pp_goals = s.stats[4];
      skater.stats.pp_assists = s.stats[5];
      skater.stats.penalty_minutes = s.stats[6];
      skater.stats.face_off_wins = s.stats[7];
      skater.stats.face_off_taken = s.stats[8];
      skater.stats.takeaways = s.stats[9];
      skater.stats.giveaways = s.stats[10];
      skater.stats.sh_goals = s.stats[11];
      skater.stats.sh_assists = s.stats[12];
      skater.stats.blocked = s.stats[13];
      skater.stats.plus_minus = s.stats[14];
      skater.stats.toi = s.stats[15];
      skater.stats.even_toi = s.stats[16];
      skater.stats.pp_toi = s.stats[17];
      skater.stats.sh_toi = s.stats[18];
      skater.stats.games = s.stats[19];
      newStat.skaters.push(skater);
    }
    state.skaterStats = newStat;
  },

  setGoalieStats(state, {stats}) {
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
      goalie.stats.penalty_minutes = s.stats[3];
      goalie.stats.shots = s.stats[4];
      goalie.stats.saves = s.stats[5];
      goalie.stats.pp_saves = s.stats[6];
      goalie.stats.sh_saves = s.stats[7];
      goalie.stats.even_saves = s.stats[8];
      goalie.stats.sh_shots_against = s.stats[9];
      goalie.stats.even_shots_against = s.stats[10];
      goalie.stats.pp_shots_against = s.stats[11];
      goalie.stats.games = s.stats[12];
      goalie.stats.wins = s.stats[13];
      goalie.stats.shutout = s.stats[14];
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
