import teamsApi from 'Api/teams';
import {logger} from 'Root/logger';
import StoreUtils from 'Store/utils';

const teamStatRanges = {
  goalsFor: [136, 258],
  goalsAgainst: [136, 259],
  shots: [1542, 2703],
  shotsAgainst: [1542, 2703],
  haGoalsFor: [68, 129],
  haGoalsAgainst: [68, 129],
  haShots: [771, 1351],
  haShotsAgainst: [771, 1351],
  winRegular: [15, 41],
  winOvertime: [1, 9],
  winShootout: [1, 9],
  loseRegular: [16, 44],
  loseOvertime: [2, 9],
  loseShootout: [1, 8],
  ppPercentage: [10, 27], // min-max, since range is small
  pkPercentage: [72, 87], // min-max, since range is small
  haPpPercentage: [10, 27], // min-max, since range is small
  haPkPercentage: [72, 87], // min-max, since range is small
  faceOffWinsPercentage: [44, 55] // min-max, since range is small
};

const state = {
  allTeams: {},
  teamStats: {},
  teamSeasonInfo: {},
  teamSeasons: {},
  teamPlayersStats: {},
  teamAllStats: {},
  standings: {},
  playOff: {},
  conferences: {},
  divisions: {},
  teamStatRanges: teamStatRanges,
  teamsComparison: {},
  teamPointsProgress: {}
};

function isCorrectTeam(teamId, stats) {
  return stats.team && stats.team.id === teamId;
}

function checkSeasonAndReturnData(state, stateName) {
  return (season) => {
    let stats = state[stateName];
    if (StoreUtils.isCorrectSeason(season, stats)) {
      return stats;
    }
    return null;
  };
}

const getters = {
  getAllTeams(state) {
    return checkSeasonAndReturnData(state, 'allTeams');
  },

  getTeamStatRange(state) {
    return (statName) => state.teamStatRanges[statName];
  },

  getTeamStats(state) {
    return checkSeasonAndReturnData(state, 'teamStats');
  },

  getTeamSeasonInfo(state) {
    return (season, teamId) => {
      let stats = state.teamSeasonInfo;
      if (StoreUtils.isCorrectSeason(season, stats) && isCorrectTeam(teamId, stats)) {
        return stats;
      }
      return null;
    };
  },

  getTeamPlayersStats(state) {
    return (season, teamId) => {
      let stats = state.teamPlayersStats;
      if (StoreUtils.isCorrectSeason(season, stats) && isCorrectTeam(teamId, stats)) {
        return stats;
      }
      return null;
    };
  },

  getTeamAllStats(state) {
    return (teamId) => {
      let stats = state.teamAllStats;
      if (isCorrectTeam(teamId, stats)) {
        return stats;
      }
      return null;
    };
  },

  getTeamsComparison(state) {
    return (season, team1Id, team2Id) => {
      let stats = state.teamsComparison;
      if (StoreUtils.isCorrectSeason(season, stats) && stats.team1.id === team1Id && stats.team2.id === team2Id) {
        return stats;
      }
      return null;
    };
  },

  getTeamSeasonChartData(state) {
    return (chartName, season, teamId) => {
      let stats = state[chartName];
      if (StoreUtils.isCorrectSeason(season, stats) && stats.tid === teamId) {
        return stats;
      }
      return null;
    };
  },

  getStandings(state) {
    return checkSeasonAndReturnData(state, 'standings');
  },

  getPlayOff(state) {
    return checkSeasonAndReturnData(state, 'playOff');
  },

  getConferenceBySerialNumber(state) {
    return (serialNum) => {
      let conferences = Object.keys(state.conferences).map((k) => Number(k));
      if (conferences.length < 2) {
        return null;
      }
      // We know there can be only 2 conferences
      let id = 0;
      if (serialNum === 1) {
        id = Math.min(conferences[0], conferences[1]);
      } else {
        id = Math.max(conferences[0], conferences[1]);
      }
      return {id: id, name: state.conferences[id]};
    };
  }
};

function getTeamsDataBySeason(actName, mutName, stateName, commit, state, reqParams) {
  logger.debug(`action: ${actName}`);
  if (reqParams.isSeasonEqual(state[stateName].season)) {
    logger.debug(`action: ${actName} data is in storage`);
    return Promise.resolve(state[stateName]);
  }
  let requestPromise = teamsApi[actName](reqParams);
  return StoreUtils.processRequest(actName, mutName, stateName, commit, state, requestPromise);
}

function getTeamDataByIdAndSeason(actName, mutName, stateName, commit, state, teamId, reqParams) {
  logger.debug(`action: ${actName}`);
  if (state[stateName].team && teamId === state[stateName].team.id &&
      reqParams.isSeasonEqual(state[stateName].season)) {
    logger.debug(`action: ${actName} data is in storage`);
    return Promise.resolve(state[stateName]);
  }
  let requestPromise = teamsApi[actName](teamId, reqParams);
  return StoreUtils.processRequest(actName, mutName, stateName, commit, state, requestPromise);
}

function getTeamDataById(actName, mutName, stateName, commit, state, teamId) {
  logger.debug(`action: ${actName}`);
  if (state[stateName].team && teamId === state[stateName].team.id) {
    logger.debug(`action: ${actName} data is in storage`);
    return Promise.resolve(state[stateName]);
  }
  let requestPromise = teamsApi[actName](teamId);
  return StoreUtils.processRequest(actName, mutName, stateName, commit, state, requestPromise);
}

const actions = {
  getAllTeams({commit, state}, {reqParams}) {
    logger.debug('action: getAllTeams');
    if (reqParams.isSeasonEqual(state.allTeams.season)) {
      logger.debug('action: getAllTeams data is in storage');
      return Promise.resolve(state.allTeams);
    }
    return teamsApi.getAllTeams(reqParams)
      .then(
        (result) => {
          logger.debug('action: getAllTeams result received');
          StoreUtils.commitNew(commit, 'setAllTeams', state.allTeams, result);
          commit('setConferences', result);
          commit('setDivisions', result);
          return state.allTeams;
        },
        (error) => {
          logger.error(`action: getAllTeams error: ${error.message}`);
        }
      );
  },

  getTeamStats({commit, state}, {reqParams}) {
    return getTeamsDataBySeason('getTeamStats', 'setTeamStats', 'teamStats', commit, state, reqParams);
  },

  getTeamSeasonInfo({commit, state}, {teamId, reqParams}) {
    return getTeamDataByIdAndSeason('getTeamSeasonInfo', 'setTeamSeasonInfo', 'teamSeasonInfo',
      commit, state, teamId, reqParams);
  },

  getTeamSeasons({commit, state}, {teamId}) {
    return getTeamDataById('getTeamSeasons', 'setTeamSeasons', 'teamSeasons', commit, state, teamId);
  },

  getTeamAllStats({commit, state}, {teamId}) {
    return getTeamDataById('getTeamAllStats', 'setTeamAllStats', 'teamAllStats', commit, state, teamId);
  },

  getTeamPlayersStats({commit, state}, {teamId, reqParams}) {
    return getTeamDataByIdAndSeason('getTeamPlayersStats', 'setTeamPlayersStats', 'teamPlayersStats',
      commit, state, teamId, reqParams);
  },

  getTeamsStandings({commit, state}, {reqParams}) {
    return getTeamsDataBySeason('getTeamsStandings', 'setStandings', 'standings', commit, state, reqParams);
  },

  getTeamsPlayOff({commit, state}, {reqParams}) {
    return getTeamsDataBySeason('getTeamsPlayOff', 'setPlayOff', 'playOff', commit, state, reqParams);
  },

  getTeamsComparison({commit, state}, {id1, id2, reqParams}) {
    logger.debug('action: getTeamsComparison');
    let tc = state.teamsComparison;
    if (tc.timestamp && id1 === tc.team1.id && id2 === tc.team2.id && reqParams.isSeasonEqual(tc.season)) {
      logger.debug('action: getTeamsComparison data is in storage');
      return Promise.resolve(tc);
    }
    let requestPromise = teamsApi.getTeamsComparison(id1, id2, reqParams);
    return StoreUtils.processRequest('getTeamsComparison', 'setTeamsComparison', 'teamsComparison',
                                     commit, state, requestPromise);
  },

  getTeamPointsProgress({commit, state}, {teamId, reqParams}) {
    return getTeamDataByIdAndSeason('getTeamPointsProgress', 'setTeamPointsProgress', 'teamPointsProgress',
      commit, state, teamId, reqParams);
  }
};

function teamStatsArrayToObject(statsArray) {
  return {
    goalsFor: statsArray[0],
    goalsAgainst: statsArray[1],
    games: statsArray[2],
    winRegular: statsArray[3],
    winOvertime: statsArray[4],
    winShootout: statsArray[5],
    loseRegular: statsArray[6],
    loseOvertime: statsArray[7],
    loseShootout: statsArray[8],
    points: statsArray[9],
    pointPercentage: statsArray[10],
    ppPercentage: statsArray[11],
    pkPercentage: statsArray[12],
    goalsForPerGame: statsArray[13],
    goalsAgainstPerGame: statsArray[14],
    shotsPerGame: statsArray[15],
    faceOffWinsPercentage: statsArray[16],
    goalsDiff: statsArray[0] - statsArray[1]
  };
}

function teamInfoArrayToObject(statsArray) {
  return {
    goalsFor: statsArray[0],
    goalsAgainst: statsArray[1],
    ppGoals: statsArray[2],
    shGoalsAgainst: statsArray[3],
    points: statsArray[4],
    pointPercentage: statsArray[5],
    ppPercentage: statsArray[6],
    pkPercentage: statsArray[7],
    goalsForPerGame: statsArray[8],
    goalsAgainstPerGame: statsArray[9],
    shotsPerGame: statsArray[10],
    faceOffWinsPercentage: statsArray[11],
    shootingPercentage: statsArray[12],
    shotsAgainstPerGame: statsArray[13],
    shotsAgainstPerGoal: statsArray[14],
    oppShootingPercentage: statsArray[15],
    scoringEfficiencyRatio: statsArray[16],
    shotEfficiencyRatio: statsArray[17],
    penaltyEfficiencyRatio: statsArray[18],
    pointsPerGame: statsArray[19],
    ppGoalsPerGame: statsArray[20],
    shGoalsAgainstPerGame: statsArray[21],
    ppPerGame: statsArray[22],
    shPerGame: statsArray[23],
    savePercentage: statsArray[24],
    oppSavePercentage: statsArray[25],
    shutouts: statsArray[26],
    oppShutouts: statsArray[27],
    shootoutWinPercentage: statsArray[28],
    homeGoals: statsArray[29],
    awayGoals: statsArray[30],
    homeGoalsAgainst: statsArray[31],
    awayGoalsAgainst: statsArray[32],
    homeShots: statsArray[33],
    awayShots: statsArray[34],
    homeShotsAgainst: statsArray[35],
    awayShotsAgainst: statsArray[36],
    homePPPercentage: statsArray[37],
    awayPPPercentage: statsArray[38],
    homePKPercentage: statsArray[39],
    awayPKPercentage: statsArray[40],
    homeWinPercentage: statsArray[41],
    awayWinPercentage: statsArray[42],
    ppPercentageRate: statsArray[43],
    ppPercentageAvg: statsArray[44],
    pkPercentageRate: statsArray[45],
    pkPercentageAvg: statsArray[46],
    goalsForPerGameRate: statsArray[47],
    goalsForPerGameAvg: statsArray[48],
    goalsAgainstPerGameRate: statsArray[49],
    goalsAgainstPerGameAvg: statsArray[50],
    faceOffWinsPercentageRate: statsArray[51],
    faceOffWinsPercentageAvg: statsArray[52],
    shootingPercentageRate: statsArray[53],
    shootingPercentageAvg: statsArray[54]
  };
}

const mutations = {
  setAllTeams(state, teams) {
    logger.debug('mutation: setAllTeams');
    let allTeams = {};
    allTeams.timestamp = teams.timestamp;
    allTeams.season = StoreUtils.convertSeason(teams.season);
    allTeams.teams = {};
    for (let t of teams.teams) {
      allTeams.teams[t.id] = t;
    }
    state.allTeams = allTeams;
  },

  setTeamStats(state, stats) {
    logger.debug('mutation: setTeamStats');
    let newStat = {};
    newStat.timestamp = stats.timestamp;
    newStat.season = StoreUtils.convertSeason(stats.season);
    newStat.teams = [];
    for (let s of stats.results) {
      let team = {
        id: s.id,
        stats: teamStatsArrayToObject(s.stats)
      };
      newStat.teams.push(team);
    }
    state.teamStats = newStat;
  },

  setTeamSeasonInfo(state, info) {
    logger.debug('mutation: setTeamSeasonInfo');
    let teamInfo = teamInfoArrayToObject(info.stats);
    teamInfo.timestamp = info.timestamp;
    teamInfo.season = StoreUtils.convertSeason(info.season);
    teamInfo.team = info.team;

    state.teamSeasonInfo = teamInfo;
  },

  setTeamSeasons(state, result) {
    logger.debug('mutation: setTeamSeasons');
    state.teamSeasons = {
      timestamp: result.timestamp,
      seasons: result.seasons.map((s) => StoreUtils.convertSeason(s)),
      team: {id: result.id}
    };
  },

  setTeamAllStats(state, stats) {
    logger.debug('mutation: setTeamAllStats');
    let newStat = {};
    newStat.timestamp = stats.timestamp;
    newStat.team = stats.team;
    newStat.seasons = [];
    for (let s of stats.results) {
      let season = {
        season: StoreUtils.convertSeason(s.season),
        stats: teamStatsArrayToObject(s.stats)
      };
      newStat.seasons.push(season);
    }
    state.teamAllStats = newStat;
  },

  setTeamPlayersStats(state, result) {
    logger.debug('mutation: setTeamPlayersStats');
    let newStat = {};
    newStat.timestamp = result.timestamp;
    newStat.team = result.team;
    newStat.season = StoreUtils.convertSeason(result.season);
    newStat.skaters = [];
    newStat.goalies = [];
    for (let s of result.skaters) {
      let skater = {
        player: s.player,
        stats: StoreUtils.skaterStatsArrayToObject(s.stats)
      };
      newStat.skaters.push(skater);
    }
    for (let g of result.goalies) {
      let goalie = {
        player: g.player,
        stats: StoreUtils.goalieStatsArrayToObject(g.stats)
      };
      newStat.goalies.push(goalie);
    }
    state.teamPlayersStats = newStat;
  },

  setStandings(state, result) {
    logger.debug('mutation: setStandings');
    state.standings = {
      timestamp: result.timestamp,
      season: StoreUtils.convertSeason(result.season),
      league: result.league,
      conferences: result.conferences,
      divisions: result.divisions,
      wildCards: result.wildCards
    };
  },

  setPlayOff(state, result) {
    logger.debug('mutation: setPlayOff');
    state.playOff = {
      timestamp: result.timestamp,
      season: StoreUtils.convertSeason(result.season),
      rounds: result.rounds
    };
  },

  setConferences(state, teams) {
    logger.debug('mutation: setConferences');
    let conf = {};
    for (let team of teams.teams) {
      if (team.cid) {
        conf[team.cid] = team.conference;
      }
    }
    state.conferences = conf;
  },

  setDivisions(state, teams) {
    logger.debug('mutation: setDivisions');
    let div = {};
    for (let team of teams.teams) {
      if (team.did) {
        div[team.did] = {name: team.division, cid: team.cid};
      }
    }
    state.divisions = div;
  },

  setTeamsComparison(state, stats) {
    logger.debug('mutation: setTeamsComparison');
    let tc = {};
    tc.timestamp = stats.timestamp;
    tc.season = StoreUtils.convertSeason(stats.season);
    tc.team1 = stats.team1;
    tc.team2 = stats.team2;
    tc.stats1 = teamInfoArrayToObject(stats.stats1);
    tc.stats2 = teamInfoArrayToObject(stats.stats2);
    tc.vs = {
      goals1: stats.vs[0],
      shots1: stats.vs[1],
      pim1: stats.vs[2],
      ppp1: stats.vs[3],
      pkp1: stats.vs[4],
      goals2: stats.vs[5],
      shots2: stats.vs[6],
      pim2: stats.vs[7],
      ppp2: stats.vs[8],
      pkp2: stats.vs[9]
    };
    tc.games = [];
    for (let s of stats.games) {
      let score = {
        date: StoreUtils.parseDate(s.date),
        winType: s.stats[0],
        homeId: s.stats[1],
        homeGoals: s.stats[2],
        homeShots: s.stats[3],
        homePpGoals: s.stats[4],
        homePpOpportunities: s.stats[5],
        homePim: s.stats[6],
        homeSvp: s.stats[7],
        awayId: s.stats[8],
        awayGoals: s.stats[9],
        awayShots: s.stats[10],
        awayPpGoals: s.stats[11],
        awayPpOpportunities: s.stats[12],
        awayPim: s.stats[13],
        awaySvp: s.stats[14]
      };
      tc.games.push(score);
    }

    state.teamsComparison = tc;
  },

  setTeamPointsProgress(state, stats) {
    logger.debug('mutation: setTeamPointsProgress');
    let season = StoreUtils.convertSeason(stats.season);
    state.teamPointsProgress = {
      timestamp: stats.timestamp,
      season: season,
      tid: stats.tid,
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
