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
  conferences: [],
  divisions: [],
  teamStatRanges: teamStatRanges,
  teamsComparison: {},
  teamPointsProgress: {}
};

function isCorrectTeam(teamId, stats) {
  return stats.team && stats.team.id === teamId;
}

const getters = {
  getAllTeams(state) {
    return (season) => {
      let stats = state.allTeams;
      if (StoreUtils.isCorrectSeason(season, stats)) {
        return stats;
      }
      return null;
    };
  },

  getTeamStatRange(state) {
    return (statName) => state.teamStatRanges[statName];
  },

  getTeamStats(state) {
    return (season) => {
      let stats = state.teamStats;
      if (StoreUtils.isCorrectSeason(season, stats)) {
        return stats;
      }
      return null;
    };
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
    if (state.allTeams.timestamp) {
      logger.debug('action: getAllTeams data is in storage');
      return Promise.resolve(state.allTeams);
    }
    return teamsApi.getAllTeams(reqParams)
      .then(
        (result) => {
          logger.debug('action: getAllTeams result received');
          StoreUtils.commitNew(commit, 'setAllTeams', state.allTeams, result);
          if (state.conferences.length === 0) {
            commit('setConferences', result);
          }
          if (state.divisions.length === 0) {
            commit('setDivisions', result);
          }
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

  getTeamsComparison({commit, state}, {team1Id, team2Id, reqParams}) {
    logger.debug('action: getTeamsComparison');
    let tc = state.teamsComparison;
    if (tc.timestamp && team1Id === tc.team1.id && team2Id === tc.team2.id && reqParams.isSeasonEqual(tc.season)) {
      logger.debug('action: getTeamsComparison data is in storage');
      return Promise.resolve(tc);
    }
    let requestPromise = teamsApi.getTeamsComparison(team1Id, team2Id, reqParams);
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
    pointPercentage: statsArray[4],
    ppPercentage: statsArray[5],
    pkPercentage: statsArray[6],
    goalsForPerGame: statsArray[7],
    goalsAgainstPerGame: statsArray[8],
    shotsPerGame: statsArray[9],
    faceOffWinsPercentage: statsArray[10],
    shootingPercentage: statsArray[11],
    shotsAgainstPerGame: statsArray[12],
    oppShootingPercentage: statsArray[13],
    scoringEfficiencyRatio: statsArray[14],
    shotEfficiencyRatio: statsArray[15],
    penaltyEfficiencyRatio: statsArray[16],
    pointsPerGame: statsArray[17],
    ppGoalsPerGame: statsArray[18],
    shGoalsAgainstPerGame: statsArray[19],
    ppPerGame: statsArray[20],
    shPerGame: statsArray[21],
    savePercentage: statsArray[22],
    oppSavePercentage: statsArray[23],
    shutouts: statsArray[24],
    homeGoals: statsArray[25],
    awayGoals: statsArray[26],
    homeGoalsAgainst: statsArray[27],
    awayGoalsAgainst: statsArray[28],
    homeShots: statsArray[29],
    awayShots: statsArray[30],
    homeShotsAgainst: statsArray[31],
    awayShotsAgainst: statsArray[32],
    homePPPercentage: statsArray[33],
    awayPPPercentage: statsArray[34],
    homePKPercentage: statsArray[35],
    awayPKPercentage: statsArray[36],
    ppPercentageRate: statsArray[37],
    ppPercentageAvg: statsArray[38],
    pkPercentageRate: statsArray[39],
    pkPercentageAvg: statsArray[40],
    goalsForPerGameRate: statsArray[41],
    goalsForPerGameAvg: statsArray[42],
    goalsAgainstPerGameRate: statsArray[43],
    goalsAgainstPerGameAvg: statsArray[44],
    faceOffWinsPercentageRate: statsArray[45],
    faceOffWinsPercentageAvg: statsArray[46],
    shootingPercentageRate: statsArray[47],
    shootingPercentageAvg: statsArray[48]
  };
}

const mutations = {
  setAllTeams(state, teams) {
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

  setConferences(state, teams) {
    logger.debug('mutation: setConferences');
    let conf = {};
    for (let team of teams.teams) {
      if (team.cid) {
        conf[team.cid] = team.conference;
      }
    }
    state.conferences = Object.keys(conf).map((key) => {
      return {id: Number(key), name: conf[key]};
    });
  },

  setDivisions(state, teams) {
    logger.debug('mutation: setDivisions');
    let div = {};
    for (let team of teams.teams) {
      if (team.did) {
        div[team.did] = {name: team.division, cid: team.cid};
      }
    }
    state.divisions = Object.keys(div).map((key) => {
      return {id: Number(key), name: div[key].name, cid: div[key].cid};
    }).sort((a, b) => a.id - b.id);
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
    tc.scores = [];
    for (let s of stats.scores) {
      let score = {
        date: StoreUtils.parseDate(s.date),
        homeTeamId: s.teams[0],
        awayTeamId: s.teams[1],
        homeTeamGoals: s.goals[0],
        awayTeamGoals: s.goals[1],
        winType: s.winType
      };
      tc.scores.push(score);
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
