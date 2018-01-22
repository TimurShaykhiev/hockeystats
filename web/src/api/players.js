import makeRequest from 'Api/request';

export default {
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
  }
};
