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
  }
};
