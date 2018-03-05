import playersApi from 'Api/players';
import {logger} from 'Root/logger';
import StoreUtils from 'Store/utils';

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
  allSkaters: {},
  allGoalies: {},
  skaterStats: {},
  goalieStats: {},
  skaterSeasonInfo: {},
  goalieSeasonInfo: {},
  skaterSeasons: {},
  goalieSeasons: {},
  skaterAllStats: {},
  goalieAllStats: {},
  skaterStatRanges: skaterStatRanges,
  skaterStatsLimits: {},
  goalieStatsLimits: {},
  skatersComparison: {},
  goaliesComparison: {},
  skaterPointsProgress: {}
};

function isCorrectPlayer(playerId, stats) {
  return stats.player && stats.player.id === playerId;
}

function getAllPlayersSeasonData(state, attrName) {
  return (season) => {
    let stats = state[attrName];
    if (StoreUtils.isCorrectSeason(season, stats)) {
      return stats;
    }
    return null;
  };
}

function getPlayerSeasonData(state, attrName) {
  return (season, playerId) => {
    let stats = state[attrName];
    if (StoreUtils.isCorrectSeason(season, stats) && isCorrectPlayer(playerId, stats)) {
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

function getPlayersCompare(state, attrName) {
  return (season, player1Id, player2Id) => {
    let stats = state[attrName];
    if (StoreUtils.isCorrectSeason(season, stats) && stats.player1.id === player1Id &&
        stats.player2.id === player2Id) {
      return stats;
    }
    return null;
  };
}

const getters = {
  getSkaterStatRange(state) {
    return (statName) => state.skaterStatRanges[statName];
  },

  getAllSkaters(state) {
    return getAllPlayersSeasonData(state, 'allSkaters');
  },

  getAllGoalies(state) {
    return getAllPlayersSeasonData(state, 'allGoalies');
  },

  getSkaterStats(state) {
    return getAllPlayersSeasonData(state, 'skaterStats');
  },

  getGoalieStats(state) {
    return getAllPlayersSeasonData(state, 'goalieStats');
  },

  getSkaterSeasonInfo(state) {
    return getPlayerSeasonData(state, 'skaterSeasonInfo');
  },

  getGoalieSeasonInfo(state) {
    return getPlayerSeasonData(state, 'goalieSeasonInfo');
  },

  getSkaterAllStats(state) {
    return getPlayerAllStats(state, 'skaterAllStats');
  },

  getGoalieAllStats(state) {
    return getPlayerAllStats(state, 'goalieAllStats');
  },

  getSkatersComparison(state) {
    return getPlayersCompare(state, 'skatersComparison');
  },

  getGoaliesComparison(state) {
    return getPlayersCompare(state, 'goaliesComparison');
  },

  getPlayerSeasonChartData(state) {
    return (chartName, season, playerId) => {
      let stats = state[chartName];
      if (StoreUtils.isCorrectSeason(season, stats) && stats.pid === playerId) {
        return stats;
      }
      return null;
    };
  }
};

function getPlayersDataBySeason(actName, mutName, stateName, commit, state, reqParams) {
  logger.debug(`action: ${actName}`);
  if (reqParams.isSeasonEqual(state[stateName].season)) {
    logger.debug(`action: ${actName} data is in storage`);
    return Promise.resolve(state[stateName]);
  }
  let requestPromise = playersApi[actName](reqParams);
  return StoreUtils.processRequest(actName, mutName, stateName, commit, state, requestPromise);
}

function getPlayerDataByIdAndSeason(actName, mutName, stateName, commit, state, playerId, reqParams) {
  logger.debug(`action: ${actName}`);
  if (state[stateName].player && playerId === state[stateName].player.id &&
      reqParams.isSeasonEqual(state[stateName].season)) {
    logger.debug(`action: ${actName} data is in storage`);
    return Promise.resolve(state[stateName]);
  }
  let requestPromise = playersApi[actName](playerId, reqParams);
  return StoreUtils.processRequest(actName, mutName, stateName, commit, state, requestPromise);
}

function getPlayerDataById(actName, mutName, stateName, commit, state, playerId) {
  logger.debug(`action: ${actName}`);
  if (state[stateName].player && playerId === state[stateName].player.id) {
    logger.debug(`action: ${actName} data is in storage`);
    return Promise.resolve(state[stateName]);
  }
  let requestPromise = playersApi[actName](playerId);
  return StoreUtils.processRequest(actName, mutName, stateName, commit, state, requestPromise);
}

function getPlayersCompareData(actName, mutName, stateName, commit, state, player1Id, player2Id, reqParams) {
  logger.debug(`action: ${actName}`);
  if (state[stateName].timestamp && player1Id === state[stateName].player1.id &&
      player2Id === state[stateName].player2.id && reqParams.isSeasonEqual(state[stateName].season)) {
    logger.debug(`action: ${actName} data is in storage`);
    return Promise.resolve(state[stateName]);
  }
  let requestPromise = playersApi[actName](player1Id, player2Id, reqParams);
  return StoreUtils.processRequest(actName, mutName, stateName, commit, state, requestPromise);
}

const actions = {
  getAllSkaters({commit, state}, {reqParams}) {
    return getPlayersDataBySeason('getAllSkaters', 'setAllSkaters', 'allSkaters', commit, state, reqParams);
  },

  getAllGoalies({commit, state}, {reqParams}) {
    return getPlayersDataBySeason('getAllGoalies', 'setAllGoalies', 'allGoalies', commit, state, reqParams);
  },

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
  },

  getSkatersComparison({commit, state}, {player1Id, player2Id, reqParams}) {
    return getPlayersCompareData('getSkatersComparison', 'setSkatersComparison', 'skatersComparison',
                                 commit, state, player1Id, player2Id, reqParams);
  },

  getGoaliesComparison({commit, state}, {player1Id, player2Id, reqParams}) {
    return getPlayersCompareData('getGoaliesComparison', 'setGoaliesComparison', 'goaliesComparison',
                                 commit, state, player1Id, player2Id, reqParams);
  },

  getSkaterStatsLimits({commit, state}, {season}) {
    logger.debug('action: getSkaterStatsLimits');
    if (StoreUtils.isCorrectSeason(season, state.skaterStatsLimits)) {
      logger.debug('action: getSkaterStatsLimits is in storage');
      return Promise.resolve();
    }
    let newState = {
      season: season,
      limits: {
        faceOffTaken: StoreUtils.getStatLimit(state.skaterStats.skaters, 'faceOffTaken')
      }
    };
    commit('setSkaterStatsLimits', newState);
    return Promise.resolve();
  },

  getGoalieStatsLimits({commit, state}, {season}) {
    logger.debug('action: getGoalieStatsLimits');
    if (StoreUtils.isCorrectSeason(season, state.goalieStatsLimits)) {
      logger.debug('action: getGoalieStatsLimits is in storage');
      return Promise.resolve();
    }
    let newState = {
      season: season,
      limits: {
        games: StoreUtils.getStatLimit(state.goalieStats.goalies, 'games')
      }
    };
    commit('setGoalieStatsLimits', newState);
    return Promise.resolve();
  },

  getSkaterPointsProgress({commit, state}, {playerId, reqParams}) {
    return getPlayerDataByIdAndSeason('getSkaterPointsProgress', 'setSkaterPointsProgress', 'skaterPointsProgress',
      commit, state, playerId, reqParams);
  }
};

function skaterInfoArrayToObject(statsArray) {
  return {
    assists: statsArray[0],
    goals: statsArray[1],
    shots: statsArray[2],
    hits: statsArray[3],
    penaltyMinutes: statsArray[4],
    takeaways: statsArray[5],
    giveaways: statsArray[6],
    blocks: statsArray[7],
    plusMinus: statsArray[8],
    points: statsArray[9],
    ppPoints: statsArray[10],
    shPoints: statsArray[11],
    turnover: statsArray[12],
    pointsPerGame: statsArray[13],
    toiPerGame: statsArray[14],
    shootingPercentage: statsArray[15],
    faceOffWinsPercentage: statsArray[16],
    pointsPer60min: statsArray[17],
    goalPercentageOfPoints: statsArray[18],
    assistPercentageOfPoints: statsArray[19],
    goalsPerGame: statsArray[20],
    goalsPer60min: statsArray[21],
    evenStrengthGoalsPercentage: statsArray[22],
    ppGoalPercentage: statsArray[23],
    assistsPerGame: statsArray[24],
    assistsPer60min: statsArray[25],
    evenAssistPercentage: statsArray[26],
    ppAssistPercentage: statsArray[27],
    shotsPerGame: statsArray[28],
    shotsPer60min: statsArray[29],
    shotsPerGoal: statsArray[30],
    turnoverPer60min: statsArray[31],
    turnoverRatio: statsArray[32],
    blocksPer60min: statsArray[33],
    hitsPer60min: statsArray[34],
    PIMsPer60min: statsArray[35],
    homeGoals: statsArray[36],
    awayGoals: statsArray[37],
    homeAssists: statsArray[38],
    awayAssists: statsArray[39],
    homePlusMinus: statsArray[40],
    awayPlusMinus: statsArray[41],
    homeTurnover: statsArray[42],
    awayTurnover: statsArray[43],
    homePointsPerGame: statsArray[44],
    awayPointsPerGame: statsArray[45],
    homePim: statsArray[46],
    awayPim: statsArray[47],
    goalsRateTotal: statsArray[48],
    assistsRateTotal: statsArray[49],
    pointsRateTotal: statsArray[50],
    plusMinusRateTotal: statsArray[51],
    turnoverRateTotal: statsArray[52],
    goalsRateTeam: statsArray[53],
    assistsRateTeam: statsArray[54],
    pointsRateTeam: statsArray[55],
    plusMinusRateTeam: statsArray[56],
    turnoverRateTeam: statsArray[57]
  };
}

function goalieInfoArrayToObject(statsArray) {
  return {
    saves: statsArray[0],
    wins: statsArray[1],
    shutout: statsArray[2],
    goalsAgainst: statsArray[3],
    gaa: statsArray[4],
    svp: statsArray[5],
    winPercentage: statsArray[6],
    evenStrengthGoalsAgainst: statsArray[7],
    ppGoalsAgainst: statsArray[8],
    shGoalsAgainst: statsArray[9],
    savesPerGame: statsArray[10],
    shotsAgainstPerGoal: statsArray[11],
    evenStrengthGoalsAgainstPercentage: statsArray[12],
    homeGaa: statsArray[13],
    awayGaa: statsArray[14],
    homeSvp: statsArray[15],
    awaySvp: statsArray[16],
    homeWinPercentage: statsArray[17],
    awayWinPercentage: statsArray[18],
    homeWins: statsArray[19],
    awayWins: statsArray[20],
    gaaRate: statsArray[21],
    svpRate: statsArray[22],
    winPercentageRate: statsArray[23],
    winsRate: statsArray[24],
    shutoutRate: statsArray[25]
  };
}

const mutations = {
  setAllSkaters(state, players) {
    logger.debug('mutation: setAllSkaters');
    let allSkaters = {};
    allSkaters.timestamp = players.timestamp;
    allSkaters.season = StoreUtils.convertSeason(players.season);
    allSkaters.players = players.players;
    state.allSkaters = allSkaters;
  },

  setAllGoalies(state, players) {
    logger.debug('mutation: setAllGoalies');
    let allGoalies = {};
    allGoalies.timestamp = players.timestamp;
    allGoalies.season = StoreUtils.convertSeason(players.season);
    allGoalies.players = players.players;
    state.allGoalies = allGoalies;
  },

  setSkaterStats(state, stats) {
    logger.debug('mutation: setSkaterStats');
    let newStat = {};
    newStat.timestamp = stats.timestamp;
    newStat.season = StoreUtils.convertSeason(stats.season);
    newStat.skaters = [];
    for (let s of stats.results) {
      let skater = {
        player: s.player,
        stats: StoreUtils.skaterStatsArrayToObject(s.stats)
      };
      newStat.skaters.push(skater);
    }
    state.skaterStats = newStat;
  },

  setGoalieStats(state, stats) {
    logger.debug('mutation: setGoalieStats');
    let newStat = {};
    newStat.timestamp = stats.timestamp;
    newStat.season = StoreUtils.convertSeason(stats.season);
    newStat.goalies = [];
    for (let s of stats.results) {
      let goalie = {
        player: s.player,
        stats: StoreUtils.goalieStatsArrayToObject(s.stats)
      };
      newStat.goalies.push(goalie);
    }
    state.goalieStats = newStat;
  },

  setSkaterSeasonInfo(state, info) {
    logger.debug('mutation: setSkaterSeasonInfo');
    let skaterInfo = skaterInfoArrayToObject(info.stats);
    skaterInfo.timestamp = info.timestamp;
    skaterInfo.season = StoreUtils.convertSeason(info.season);
    skaterInfo.player = info.player;

    state.skaterSeasonInfo = skaterInfo;
  },

  setGoalieSeasonInfo(state, info) {
    logger.debug('mutation: setGoalieSeasonInfo');
    let goalieInfo = goalieInfoArrayToObject(info.stats);
    goalieInfo.timestamp = info.timestamp;
    goalieInfo.season = StoreUtils.convertSeason(info.season);
    goalieInfo.player = info.player;

    state.goalieSeasonInfo = goalieInfo;
  },

  setSkaterSeasons(state, result) {
    logger.debug('mutation: setSkaterSeasons');
    state.skaterSeasons = {
      timestamp: result.timestamp,
      seasons: result.seasons.map((s) => StoreUtils.convertSeason(s)),
      player: {id: result.id}
    };
  },

  setGoalieSeasons(state, result) {
    logger.debug('mutation: setGoalieSeasons');
    state.goalieSeasons = {
      timestamp: result.timestamp,
      seasons: result.seasons.map((s) => StoreUtils.convertSeason(s)),
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
        season: StoreUtils.convertSeason(s.season),
        teamId: s.tid,
        stats: StoreUtils.skaterStatsArrayToObject(s.stats)
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
        season: StoreUtils.convertSeason(s.season),
        teamId: s.tid,
        stats: StoreUtils.goalieStatsArrayToObject(s.stats)
      };
      newStat.seasons.push(season);
    }
    state.goalieAllStats = newStat;
  },

  setSkatersComparison(state, stats) {
    logger.debug('mutation: setSkatersComparison');
    let sc = {};
    sc.timestamp = stats.timestamp;
    sc.season = StoreUtils.convertSeason(stats.season);
    sc.player1 = stats.player1;
    sc.player2 = stats.player2;
    sc.stats1 = skaterInfoArrayToObject(stats.stats1);
    sc.stats2 = skaterInfoArrayToObject(stats.stats2);

    state.skatersComparison = sc;
  },

  setGoaliesComparison(state, stats) {
    logger.debug('mutation: setGoaliesComparison');
    let gc = {};
    gc.timestamp = stats.timestamp;
    gc.season = StoreUtils.convertSeason(stats.season);
    gc.player1 = stats.player1;
    gc.player2 = stats.player2;
    gc.stats1 = goalieInfoArrayToObject(stats.stats1);
    gc.stats2 = goalieInfoArrayToObject(stats.stats2);

    state.goaliesComparison = gc;
  },

  setSkaterStatsLimits(state, stats) {
    logger.debug('mutation: setSkaterStatsLimits');
    state.skaterStatsLimits = stats;
  },

  setGoalieStatsLimits(state, stats) {
    logger.debug('mutation: setGoalieStatsLimits');
    state.goalieStatsLimits = stats;
  },

  setSkaterPointsProgress(state, stats) {
    logger.debug('mutation: setSkaterPointsProgress');
    let season = StoreUtils.convertSeason(stats.season);
    state.skaterPointsProgress = {
      timestamp: stats.timestamp,
      season: season,
      pid: stats.pid,
      data: StoreUtils.prepareLineChartData(stats.data, season.start, stats.interval)
    };
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
