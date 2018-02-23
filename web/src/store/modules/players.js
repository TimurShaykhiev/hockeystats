import playersApi from 'Api/players';
import {logger} from 'Root/logger';
import {processRequest, skaterStatsArrayToObject, goalieStatsArrayToObject, isCorrectSeason} from 'Store/utils';

// Ranges calculated from all results. 5p - 95p.
const skaterStatRanges = {
  assists: [0, 36],
  goals: [0, 24],
  haAssists: [0, 36],
  haGoals: [0, 24],
  shots: [1, 206],
  ppGoals: [0, 7],
  penaltyMinutes: [0, 73],
  haPenaltyMinutes: [0, 73],
  shGoals: [0, 1],
  plusMinus: [-15, 16],
  haPlusMinus: [-15, 16],
  games: [2, 82],
  faceOffWinsPercentage: [0, 55], // 10p - 90p
  turnover: [-30, 17],
  haTurnover: [-30, 17],
  haPointsPerGame: [0, 1]
};

const state = {
  skaterStats: {},
  goalieStats: {},
  skaterSeasonInfo: {},
  goalieSeasonInfo: {},
  skaterSeasons: {},
  goalieSeasons: {},
  skaterAllStats: {},
  goalieAllStats: {},
  skaterStatRanges: skaterStatRanges
};

function isCorrectPlayer(playerId, stats) {
  return stats.player && stats.player.id === playerId;
}

function getPlayerStats(state, attrName) {
  return (season) => {
    let stats = state[attrName];
    if (isCorrectSeason(season, stats)) {
      return stats;
    }
    return null;
  };
}

function getPlayerSeasonInfo(state, attrName) {
  return (season, playerId) => {
    let stats = state[attrName];
    if (isCorrectSeason(season, stats) && isCorrectPlayer(playerId, stats)) {
      return stats;
    }
    return null;
  };
}

function getPlayerAllStats(state, attrName) {
  return (playerId) => {
    let stats = state[attrName];
    if (isCorrectPlayer(playerId, stats)) {
      return stats;
    }
    return null;
  };
}

const getters = {
  getSkaterStatRange(state) {
    return (statName) => state.skaterStatRanges[statName];
  },

  getSkaterStats(state) {
    return getPlayerStats(state, 'skaterStats');
  },

  getGoalieStats(state) {
    return getPlayerStats(state, 'goalieStats');
  },

  getSkaterSeasonInfo(state) {
    return getPlayerSeasonInfo(state, 'skaterSeasonInfo');
  },

  getGoalieSeasonInfo(state) {
    return getPlayerSeasonInfo(state, 'goalieSeasonInfo');
  },

  getSkaterAllStats(state) {
    return getPlayerAllStats(state, 'skaterAllStats');
  },

  getGoalieAllStats(state) {
    return getPlayerAllStats(state, 'goalieAllStats');
  }
};

function getPlayersDataBySeason(actName, mutName, stateName, commit, state, reqParams) {
  logger.debug(`action: ${actName}`);
  if (reqParams.isSeasonEqual(state[stateName].season)) {
    logger.debug(`action: ${actName} data is in storage`);
    return Promise.resolve(state[stateName]);
  }
  let requestPromise = playersApi[actName](reqParams);
  return processRequest(actName, mutName, stateName, commit, state, requestPromise);
}

function getPlayerDataByIdAndSeason(actName, mutName, stateName, commit, state, playerId, reqParams) {
  logger.debug(`action: ${actName}`);
  if (state[stateName].player && playerId === state[stateName].player.id &&
      reqParams.isSeasonEqual(state[stateName].season)) {
    logger.debug(`action: ${actName} data is in storage`);
    return Promise.resolve(state[stateName]);
  }
  let requestPromise = playersApi[actName](playerId, reqParams);
  return processRequest(actName, mutName, stateName, commit, state, requestPromise);
}

function getPlayerDataById(actName, mutName, stateName, commit, state, playerId) {
  logger.debug(`action: ${actName}`);
  if (state[stateName].player && playerId === state[stateName].player.id) {
    logger.debug(`action: ${actName} data is in storage`);
    return Promise.resolve(state[stateName]);
  }
  let requestPromise = playersApi[actName](playerId);
  return processRequest(actName, mutName, stateName, commit, state, requestPromise);
}

const actions = {
  getSkaterStats({commit, state}, {reqParams}) {
    return getPlayersDataBySeason('getSkaterStats', 'setSkaterStats', 'skaterStats', commit, state, reqParams);
  },

  getGoalieStats({commit, state}, {reqParams}) {
    return getPlayersDataBySeason('getGoalieStats', 'setGoalieStats', 'goalieStats', commit, state, reqParams);
  },

  getSkaterSeasonInfo({commit, state}, {playerId, reqParams}) {
    return getPlayerDataByIdAndSeason('getSkaterSeasonInfo', 'setSkaterSeasonInfo', 'skaterSeasonInfo',
      commit, state, playerId, reqParams);
  },

  getGoalieSeasonInfo({commit, state}, {playerId, reqParams}) {
    return getPlayerDataByIdAndSeason('getGoalieSeasonInfo', 'setGoalieSeasonInfo', 'goalieSeasonInfo',
      commit, state, playerId, reqParams);
  },

  getSkaterSeasons({commit, state}, {playerId}) {
    return getPlayerDataById('getSkaterSeasons', 'setSkaterSeasons', 'skaterSeasons', commit, state, playerId);
  },

  getGoalieSeasons({commit, state}, {playerId}) {
    return getPlayerDataById('getGoalieSeasons', 'setGoalieSeasons', 'goalieSeasons', commit, state, playerId);
  },

  getSkaterAllStats({commit, state}, {playerId}) {
    return getPlayerDataById('getSkaterAllStats', 'setSkaterAllStats', 'skaterAllStats', commit, state, playerId);
  },

  getGoalieAllStats({commit, state}, {playerId}) {
    return getPlayerDataById('getGoalieAllStats', 'setGoalieAllStats', 'goalieAllStats', commit, state, playerId);
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
      let skater = {
        player: s.player,
        stats: skaterStatsArrayToObject(s.stats)
      };
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
      let goalie = {
        player: s.player,
        stats: goalieStatsArrayToObject(s.stats)
      };
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
    skaterInfo.homeGoals = info.stats[36];
    skaterInfo.awayGoals = info.stats[37];
    skaterInfo.homeAssists = info.stats[38];
    skaterInfo.awayAssists = info.stats[39];
    skaterInfo.homePlusMinus = info.stats[40];
    skaterInfo.awayPlusMinus = info.stats[41];
    skaterInfo.homeTurnover = info.stats[42];
    skaterInfo.awayTurnover = info.stats[43];
    skaterInfo.homePointsPerGame = info.stats[44];
    skaterInfo.awayPointsPerGame = info.stats[45];
    skaterInfo.homePim = info.stats[46];
    skaterInfo.awayPim = info.stats[47];
    skaterInfo.goalsRateTotal = info.stats[48];
    skaterInfo.assistsRateTotal = info.stats[49];
    skaterInfo.pointsRateTotal = info.stats[50];
    skaterInfo.plusMinusRateTotal = info.stats[51];
    skaterInfo.turnoverRateTotal = info.stats[52];
    skaterInfo.goalsRateTeam = info.stats[53];
    skaterInfo.assistsRateTeam = info.stats[54];
    skaterInfo.pointsRateTeam = info.stats[55];
    skaterInfo.plusMinusRateTeam = info.stats[56];
    skaterInfo.turnoverRateTeam = info.stats[57];

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
    goalieInfo.homeGaa = info.stats[13];
    goalieInfo.awayGaa = info.stats[14];
    goalieInfo.homeSvp = info.stats[15];
    goalieInfo.awaySvp = info.stats[16];
    goalieInfo.homeWinPercentage = info.stats[17];
    goalieInfo.awayWinPercentage = info.stats[18];
    goalieInfo.homeWins = info.stats[19];
    goalieInfo.awayWins = info.stats[20];
    goalieInfo.gaaRate = info.stats[21];
    goalieInfo.svpRate = info.stats[22];
    goalieInfo.winPercentageRate = info.stats[23];
    goalieInfo.winsRate = info.stats[24];
    goalieInfo.shutoutRate = info.stats[25];

    state.goalieSeasonInfo = goalieInfo;
  },

  setSkaterSeasons(state, result) {
    logger.debug('mutation: setSkaterSeasons');
    state.skaterSeasons = {
      timestamp: result.timestamp,
      seasons: result.seasons,
      player: {id: result.id}
    };
  },

  setGoalieSeasons(state, result) {
    logger.debug('mutation: setGoalieSeasons');
    state.goalieSeasons = {
      timestamp: result.timestamp,
      seasons: result.seasons,
      player: {id: result.id}
    };
  },

  setSkaterAllStats(state, stats) {
    logger.debug('mutation: setSkaterAllStats');
    let newStat = {};
    newStat.timestamp = stats.timestamp;
    newStat.player = stats.player;
    newStat.seasons = [];
    for (let s of stats.results) {
      let season = {
        season: s.season,
        teamId: s.tid,
        stats: skaterStatsArrayToObject(s.stats)
      };
      newStat.seasons.push(season);
    }
    state.skaterAllStats = newStat;
  },

  setGoalieAllStats(state, stats) {
    logger.debug('mutation: setGoalieAllStats');
    let newStat = {};
    newStat.timestamp = stats.timestamp;
    newStat.player = stats.player;
    newStat.seasons = [];
    for (let s of stats.results) {
      let season = {
        season: s.season,
        teamId: s.tid,
        stats: goalieStatsArrayToObject(s.stats)
      };
      newStat.seasons.push(season);
    }
    state.goalieAllStats = newStat;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
