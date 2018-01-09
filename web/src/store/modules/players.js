import playersApi from 'Api/players';
import {logger} from 'Root/logger';
import {commitNew} from 'Store/utils';

const state = {
  skaterStats: {},
  goalieStats: {},
  skaterSeasonInfo: {},
  goalieSeasonInfo: {},
  skaterSeasons: {},
  goalieSeasons: {}
};

const getters = {
};

function getPlayersStats(actName, mutName, stateName, commit, state, reqParams) {
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

function getPlayerSeasonInfo(actName, mutName, stateName, commit, state, playerId, reqParams) {
  logger.debug(`action: ${actName}`);
  if (state[stateName].player && playerId === state[stateName].player.id &&
      reqParams.isSeasonEqual(state[stateName].season)) {
    logger.debug(`action: ${actName} player info is in storage`);
    return Promise.resolve(state[stateName]);
  }
  return playersApi[actName](playerId, reqParams)
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

function getPlayerSeasons(actName, mutName, stateName, commit, state, playerId) {
  logger.debug(`action: ${actName}`);
  if (playerId === state[stateName].playerId) {
    logger.debug(`action: ${actName} player seasons in storage`);
    return Promise.resolve(state[stateName]);
  }
  return playersApi[actName](playerId)
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
    return getPlayersStats('getSkaterStats', 'setSkaterStats', 'skaterStats', commit, state, reqParams);
  },

  getGoalieStats({commit, state}, {reqParams}) {
    return getPlayersStats('getGoalieStats', 'setGoalieStats', 'goalieStats', commit, state, reqParams);
  },

  getSkaterSeasonInfo({commit, state}, {playerId, reqParams}) {
    return getPlayerSeasonInfo('getSkaterSeasonInfo', 'setSkaterSeasonInfo', 'skaterSeasonInfo',
      commit, state, playerId, reqParams);
  },

  getGoalieSeasonInfo({commit, state}, {playerId, reqParams}) {
    return getPlayerSeasonInfo('getGoalieSeasonInfo', 'setGoalieSeasonInfo', 'goalieSeasonInfo',
      commit, state, playerId, reqParams);
  },

  getSkaterSeasons({commit, state}, {playerId}) {
    return getPlayerSeasons('getSkaterSeasons', 'setSkaterSeasons', 'skaterSeasons',
      commit, state, playerId);
  },

  getGoalieSeasons({commit, state}, {playerId}) {
    return getPlayerSeasons('getGoalieSeasons', 'setGoalieSeasons', 'goalieSeasons',
      commit, state, playerId);
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
  },

  setSkaterSeasonInfo(state, info) {
    logger.debug('mutation: setSkaterSeasonInfo');
    let skaterInfo = {};
    skaterInfo.timestamp = info.timestamp;
    skaterInfo.season = info.season;
    skaterInfo.player = info.player;

    skaterInfo.assists = info.stats[0];
    skaterInfo.goals = info.stats[1];
    skaterInfo.shots = info.stats[2];
    skaterInfo.hits = info.stats[3];
    skaterInfo.penaltyMinutes = info.stats[4];
    skaterInfo.takeaways = info.stats[5];
    skaterInfo.giveaways = info.stats[6];
    skaterInfo.blocks = info.stats[7];
    skaterInfo.plusMinus = info.stats[8];
    skaterInfo.points = info.stats[9];
    skaterInfo.ppPoints = info.stats[10];
    skaterInfo.shPoints = info.stats[11];
    skaterInfo.turnover = info.stats[12];
    skaterInfo.pointsPerGame = info.stats[13];
    skaterInfo.toiPerGame = info.stats[14];
    skaterInfo.shootingPercentage = info.stats[15];
    skaterInfo.faceOffWinsPercentage = info.stats[16];
    skaterInfo.pointsPer60min = info.stats[17];
    skaterInfo.goalPercentageOfPoints = info.stats[18];
    skaterInfo.assistPercentageOfPoints = info.stats[19];
    skaterInfo.goalsPerGame = info.stats[20];
    skaterInfo.goalsPer60min = info.stats[21];
    skaterInfo.evenStrengthGoalsPercentage = info.stats[22];
    skaterInfo.ppGoalPercentage = info.stats[23];
    skaterInfo.assistsPerGame = info.stats[24];
    skaterInfo.assistsPer60min = info.stats[25];
    skaterInfo.evenAssistPercentage = info.stats[26];
    skaterInfo.ppAssistPercentage = info.stats[27];
    skaterInfo.shotsPerGame = info.stats[28];
    skaterInfo.shotsPer60min = info.stats[29];
    skaterInfo.shotsPerGoal = info.stats[30];
    skaterInfo.turnoverPer60min = info.stats[31];
    skaterInfo.turnoverRatio = info.stats[32];
    skaterInfo.blocksPer60min = info.stats[33];
    skaterInfo.hitsPer60min = info.stats[34];
    skaterInfo.PIMsPer60min = info.stats[35];
    skaterInfo.goalsRateTotal = info.stats[36];
    skaterInfo.assistsRateTotal = info.stats[37];
    skaterInfo.pointsRateTotal = info.stats[38];
    skaterInfo.plusMinusRateTotal = info.stats[39];
    skaterInfo.turnoverRateTotal = info.stats[40];
    skaterInfo.goalsRateTeam = info.stats[41];
    skaterInfo.assistsRateTeam = info.stats[42];
    skaterInfo.pointsRateTeam = info.stats[43];
    skaterInfo.plusMinusRateTeam = info.stats[44];
    skaterInfo.turnoverRateTeam = info.stats[45];

    state.skaterSeasonInfo = skaterInfo;
  },

  setGoalieSeasonInfo(state, info) {
    logger.debug('mutation: setGoalieSeasonInfo');
    let goalieInfo = {};
    goalieInfo.timestamp = info.timestamp;
    goalieInfo.season = info.season;
    goalieInfo.player = info.player;

    goalieInfo.saves = info.stats[0];
    goalieInfo.wins = info.stats[1];
    goalieInfo.shutout = info.stats[2];
    goalieInfo.goalsAgainst = info.stats[3];
    goalieInfo.gaa = info.stats[4];
    goalieInfo.svp = info.stats[5];
    goalieInfo.winPercentage = info.stats[6];
    goalieInfo.evenStrengthGoalsAgainst = info.stats[7];
    goalieInfo.ppGoalsAgainst = info.stats[8];
    goalieInfo.shGoalsAgainst = info.stats[9];
    goalieInfo.savesPerGame = info.stats[10];
    goalieInfo.shotsAgainstPerGoal = info.stats[11];
    goalieInfo.evenStrengthGoalsAgainstPercentage = info.stats[12];
    goalieInfo.gaaRate = info.stats[13];
    goalieInfo.svpRate = info.stats[14];
    goalieInfo.winPercentageRate = info.stats[15];
    goalieInfo.winsRate = info.stats[16];
    goalieInfo.shutoutRate = info.stats[17];

    state.goalieSeasonInfo = goalieInfo;
  },

  setSkaterSeasons(state, result) {
    logger.debug('mutation: setSkaterSeasons');
    state.skaterSeasons = {
      timestamp: result.timestamp,
      seasons: result.seasons,
      playerId: result.id
    };
  },

  setGoalieSeasons(state, result) {
    logger.debug('mutation: setGoalieSeasons');
    state.goalieSeasons = {
      timestamp: result.timestamp,
      seasons: result.seasons,
      playerId: result.id
    };
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
