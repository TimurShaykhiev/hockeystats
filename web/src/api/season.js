import makeRequest from 'Api/request';

export default {
  getCurrentSeason() {
    return makeRequest({path: ['season', 'current']});
  },

  getAllSeasons() {
    return makeRequest({path: ['season', 'all']});
  },

  getSeasonPenalties(reqParams) {
    let reqData = {
      path: ['season', 'charts', 'penalties'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  }
};
