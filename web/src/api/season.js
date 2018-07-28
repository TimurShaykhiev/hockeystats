import makeRequest from 'Api/request';

export default {
  getCurrentSeason() {
    return makeRequest({path: ['season', 'current']});
  },

  getAllSeasons() {
    return makeRequest({path: ['season', 'all']});
  },

  getSeasonStats() {
    return makeRequest({path: ['stats', 'seasons']});
  },

  getSeasonInfo(reqParams) {
    let reqData = {
      path: ['season', 'stats'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  },

  getSeasonPenalties(reqParams) {
    let reqData = {
      path: ['season', 'charts', 'penalties'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  }
};
