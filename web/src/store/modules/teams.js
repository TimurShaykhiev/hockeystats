import teamsApi from 'Api/teams';
import {logger} from 'Root/logger';
import {commitNew, getPercentage} from 'Store/utils';

const state = {
  teamStats: {},
  conferences: []
};

const getters = {
};

const actions = {
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
          if (state.conferences.length === 0) {
            commit('setConferences', result);
          }
          return state.teamStats;
        },
        (error) => {
          logger.error(`action: getTeamStats error: ${error.message}`);
        }
      );
  }
};

const mutations = {
  setTeamStats(state, stats) {
    logger.debug('mutation: setTeamStats');
    let newStat = {};
    newStat.timestamp = stats.timestamp;
    newStat.season = stats.season;
    newStat.teams = [];
    for (let s of stats.results) {
      let team = {team: s.team, stats: {}};
      team.stats.goalsFor = s.stats[0];
      team.stats.goalsAgainst = s.stats[1];
      team.stats.shots = s.stats[2];
      team.stats.ppGoals = s.stats[3];
      team.stats.ppOpportunities = s.stats[4];
      team.stats.shGoalsAgainst = s.stats[5];
      team.stats.shOpportunities = s.stats[6];
      team.stats.faceOffWins = s.stats[7];
      team.stats.faceOffTaken = s.stats[8];
      team.stats.blocked = s.stats[9];
      team.stats.takeaways = s.stats[10];
      team.stats.giveaways = s.stats[11];
      team.stats.hits = s.stats[12];
      team.stats.penaltyMinutes = s.stats[13];
      team.stats.games = s.stats[14];
      team.stats.winRegular = s.stats[15];
      team.stats.winOvertime = s.stats[16];
      team.stats.winShootout = s.stats[17];
      team.stats.loseRegular = s.stats[18];
      team.stats.loseOvertime = s.stats[19];
      team.stats.loseShootout = s.stats[20];
      // Calculate some stats
      team.stats.points = (team.stats.winRegular + team.stats.winOvertime + team.stats.winShootout) * 2 +
                          team.stats.loseOvertime + team.stats.loseShootout;
      team.stats.pointPercentage = getPercentage(team.stats.points, team.stats.games * 2);
      team.stats.goalsForPerGame = getPercentage(team.stats.goalsFor, team.stats.games, true);
      team.stats.goalsAgainstPerGame = getPercentage(team.stats.goalsAgainst, team.stats.games, true);
      team.stats.ppPercentage = getPercentage(team.stats.ppGoals, team.stats.ppOpportunities);
      team.stats.pkPercentage = 100 - getPercentage(team.stats.shGoalsAgainst, team.stats.shOpportunities);
      team.stats.shotsPerGame = getPercentage(team.stats.shots, team.stats.games, true);
      team.stats.faceOffWinsPercentage = getPercentage(team.stats.faceOffWins, team.stats.faceOffTaken);

      newStat.teams.push(team);
    }
    state.teamStats = newStat;
  },

  setConferences(state, stats) {
    logger.debug('mutation: setConferences');
    let conf = {};
    for (let s of stats.results) {
      conf[s.team.cid] = s.team.conference;
    }
    state.conferences = Object.keys(conf).map((key) => {
      return {id: Number(key), name: conf[key]};
    });
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
