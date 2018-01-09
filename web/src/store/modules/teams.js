import teamsApi from 'Api/teams';
import {logger} from 'Root/logger';
import {commitNew} from 'Store/utils';

const state = {
  allTeams: {},
  teamStats: {},
  teamSeasonInfo: {},
  teamSeasons: {},
  conferences: [],
  divisions: []
};

const getters = {
};

const actions = {
  getAllTeams({commit, state}, {reqParams}) {
    logger.debug('action: getAllTeams');
    if (state.allTeams.timestamp) {
      logger.debug('action: getAllTeams all teams are in storage');
      return Promise.resolve(state.allTeams);
    }
    return teamsApi.getAllTeams(reqParams)
      .then(
        (result) => {
          logger.debug('action: getAllTeams result received');
          commitNew(commit, 'setAllTeams', state.allTeams, result);
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
    logger.debug('action: getTeamStats');
    if (reqParams.isSeasonEqual(state.teamStats.season)) {
      logger.debug('action: getTeamStats season is in storage');
      return Promise.resolve(state.teamStats);
    }
    return teamsApi.getTeamStats(reqParams)
      .then(
        (result) => {
          logger.debug('action: getTeamStats result received');
          commitNew(commit, 'setTeamStats', state.teamStats, result);
          return state.teamStats;
        },
        (error) => {
          logger.error(`action: getTeamStats error: ${error.message}`);
        }
      );
  },

  getTeamSeasonInfo({commit, state}, {teamId, reqParams}) {
    logger.debug('action: getTeamSeasonInfo');
    if (state.teamSeasonInfo.team && teamId === state.teamSeasonInfo.team.id &&
        reqParams.isSeasonEqual(state.teamSeasonInfo.season)) {
      logger.debug('action: getTeamSeasonInfo team info is in storage');
      return Promise.resolve(state.teamSeasonInfo);
    }
    return teamsApi.getTeamSeasonInfo(teamId, reqParams)
      .then(
        (result) => {
          logger.debug('action: getTeamSeasonInfo result received');
          commitNew(commit, 'setTeamSeasonInfo', state.teamSeasonInfo, result);
          return state.teamSeasonInfo;
        },
        (error) => {
          logger.error(`action: getTeamSeasonInfo error: ${error.message}`);
        }
      );
  },

  getTeamSeasons({commit, state}, {teamId}) {
    logger.debug('action: getTeamSeasons');
    if (teamId === state.teamSeasons.teamId) {
      logger.debug('action: getTeamSeasons team seasons in storage');
      return Promise.resolve(state.teamSeasons);
    }
    return teamsApi.getTeamSeasons(teamId)
      .then(
        (result) => {
          logger.debug('action: getTeamSeasons result received');
          commitNew(commit, 'setTeamSeasons', state.teamSeasons, result);
          return state.teamSeasons;
        },
        (error) => {
          logger.error(`action: getTeamSeasons error: ${error.message}`);
        }
      );
  }
};

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
      let team = {id: s.id, stats: {}};
      team.stats.goalsFor = s.stats[0];
      team.stats.goalsAgainst = s.stats[1];
      team.stats.games = s.stats[2];
      team.stats.winRegular = s.stats[3];
      team.stats.winOvertime = s.stats[4];
      team.stats.winShootout = s.stats[5];
      team.stats.loseRegular = s.stats[6];
      team.stats.loseOvertime = s.stats[7];
      team.stats.loseShootout = s.stats[8];
      team.stats.points = s.stats[9];
      team.stats.pointPercentage = s.stats[10];
      team.stats.ppPercentage = s.stats[11];
      team.stats.pkPercentage = s.stats[12];
      team.stats.goalsForPerGame = s.stats[13];
      team.stats.goalsAgainstPerGame = s.stats[14];
      team.stats.shotsPerGame = s.stats[15];
      team.stats.faceOffWinsPercentage = s.stats[16];

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
      teamId: result.id
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
