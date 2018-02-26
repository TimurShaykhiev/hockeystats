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
  teamStatRanges: teamStatRanges
};

function isCorrectTeam(teamId, stats) {
  return stats.team && stats.team.id === teamId;
}

const getters = {
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

const mutations = {
  setAllTeams(state, teams) {
    let allTeams = {};
    allTeams.timestamp = teams.timestamp;
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
    newStat.season = stats.season;
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
    let teamInfo = {};
    teamInfo.timestamp = info.timestamp;
    teamInfo.season = info.season;
    teamInfo.team = info.team;

    teamInfo.goalsFor = info.stats[0];
    teamInfo.goalsAgainst = info.stats[1];
    teamInfo.ppGoals = info.stats[2];
    teamInfo.shGoalsAgainst = info.stats[3];
    teamInfo.pointPercentage = info.stats[4];
    teamInfo.ppPercentage = info.stats[5];
    teamInfo.pkPercentage = info.stats[6];
    teamInfo.goalsForPerGame = info.stats[7];
    teamInfo.goalsAgainstPerGame = info.stats[8];
    teamInfo.shotsPerGame = info.stats[9];
    teamInfo.faceOffWinsPercentage = info.stats[10];
    teamInfo.shootingPercentage = info.stats[11];
    teamInfo.shotsAgainstPerGame = info.stats[12];
    teamInfo.oppShootingPercentage = info.stats[13];
    teamInfo.scoringEfficiencyRatio = info.stats[14];
    teamInfo.shotEfficiencyRatio = info.stats[15];
    teamInfo.penaltyEfficiencyRatio = info.stats[16];
    teamInfo.pointsPerGame = info.stats[17];
    teamInfo.ppGoalsPerGame = info.stats[18];
    teamInfo.shGoalsAgainstPerGame = info.stats[19];
    teamInfo.ppPerGame = info.stats[20];
    teamInfo.shPerGame = info.stats[21];
    teamInfo.savePercentage = info.stats[22];
    teamInfo.oppSavePercentage = info.stats[23];
    teamInfo.shutouts = info.stats[24];
    teamInfo.homeGoals = info.stats[25];
    teamInfo.awayGoals = info.stats[26];
    teamInfo.homeGoalsAgainst = info.stats[27];
    teamInfo.awayGoalsAgainst = info.stats[28];
    teamInfo.homeShots = info.stats[29];
    teamInfo.awayShots = info.stats[30];
    teamInfo.homeShotsAgainst = info.stats[31];
    teamInfo.awayShotsAgainst = info.stats[32];
    teamInfo.homePPPercentage = info.stats[33];
    teamInfo.awayPPPercentage = info.stats[34];
    teamInfo.homePKPercentage = info.stats[35];
    teamInfo.awayPKPercentage = info.stats[36];
    teamInfo.ppPercentageRate = info.stats[37];
    teamInfo.ppPercentageAvg = info.stats[38];
    teamInfo.pkPercentageRate = info.stats[39];
    teamInfo.pkPercentageAvg = info.stats[40];
    teamInfo.goalsForPerGameRate = info.stats[41];
    teamInfo.goalsForPerGameAvg = info.stats[42];
    teamInfo.goalsAgainstPerGameRate = info.stats[43];
    teamInfo.goalsAgainstPerGameAvg = info.stats[44];
    teamInfo.faceOffWinsPercentageRate = info.stats[45];
    teamInfo.faceOffWinsPercentageAvg = info.stats[46];
    teamInfo.shootingPercentageRate = info.stats[47];
    teamInfo.shootingPercentageAvg = info.stats[48];

    state.teamSeasonInfo = teamInfo;
  },

  setTeamSeasons(state, result) {
    logger.debug('mutation: setTeamSeasons');
    state.teamSeasons = {
      timestamp: result.timestamp,
      seasons: result.seasons,
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
        season: s.season,
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
    newStat.season = result.season;
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
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
