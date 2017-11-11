import makeRequest from 'Api/request';

export default {
  getTeamStats(reqParams) {
    let reqData = {
      path: ['stats', 'teams'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  }
};
