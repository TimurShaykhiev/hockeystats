import makeRequest from 'Api/request';

export default {
  getAllTeams(reqParams) {
    let reqData = {
      path: ['teams'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getTeamStats(reqParams) {
    let reqData = {
      path: ['stats', 'teams'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getTeamSeasonInfo(teamId, reqParams) {
    let reqData = {
      path: ['team', teamId, 'stats'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getTeamSeasons(teamId) {
    return makeRequest({path: ['team', teamId, 'seasons']});
  },

  getTeamAllStats(teamId) {
    return makeRequest({path: ['team', teamId, 'all-stats']});
  },

  getTeamPlayersStats(teamId, reqParams) {
    let reqData = {
      path: ['team', teamId, 'players', 'stats'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getTeamsComparison(team1Id, team2Id, reqParams) {
    let reqData = {
      path: ['team', team1Id, 'compare', team2Id],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getTeamPointsProgress(teamId, reqParams) {
    let reqData = {
      path: ['team', teamId, 'charts', 'points-progress'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getTeamPenalties(teamId, reqParams) {
    let reqData = {
      path: ['team', teamId, 'charts', 'penalties'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getTeamsStandings(reqParams) {
    let reqData = {
      path: ['teams', 'standings'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getTeamsPlayOff(reqParams) {
    let reqData = {
      path: ['teams', 'play-off'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  }
};
