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
  }
};
