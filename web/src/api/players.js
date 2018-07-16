import makeRequest from 'Api/request';

export default {
  getAllSkaters(reqParams) {
    let reqData = {
      path: ['skaters'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getAllGoalies(reqParams) {
    let reqData = {
      path: ['goalies'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getSkaterStats(reqParams) {
    let reqData = {
      path: ['stats', 'skaters'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getGoalieStats(reqParams) {
    let reqData = {
      path: ['stats', 'goalies'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getSkaterSeasonInfo(playerId, reqParams) {
    let reqData = {
      path: ['skater', playerId, 'stats'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getGoalieSeasonInfo(playerId, reqParams) {
    let reqData = {
      path: ['goalie', playerId, 'stats'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getSkaterSeasons(playerId) {
    return makeRequest({path: ['skater', playerId, 'seasons']});
  },

  getGoalieSeasons(playerId) {
    return makeRequest({path: ['goalie', playerId, 'seasons']});
  },

  getSkaterAllStats(playerId) {
    return makeRequest({path: ['skater', playerId, 'all-stats']});
  },

  getGoalieAllStats(playerId) {
    return makeRequest({path: ['goalie', playerId, 'all-stats']});
  },

  getSkatersComparison(player1Id, player2Id, reqParams) {
    let reqData = {
      path: ['skater', player1Id, 'compare', player2Id],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getGoaliesComparison(player1Id, player2Id, reqParams) {
    let reqData = {
      path: ['goalie', player1Id, 'compare', player2Id],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getSkaterPointsProgress(playerId, reqParams) {
    let reqData = {
      path: ['skater', playerId, 'charts', 'points-progress'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getSkatersPenaltyDrewBy(reqParams) {
    let reqData = {
      path: ['skaters', 'charts', 'penalty-drew-by'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  }
};
