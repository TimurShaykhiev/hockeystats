import teamsApi from 'Api/teams';
import {logger} from 'Root/logger';
import {commitNew} from 'Store/utils';

const state = {
  allTeams: {},
  teamStats: {},
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
      return Promise.resolve(state['teamStats']);
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
