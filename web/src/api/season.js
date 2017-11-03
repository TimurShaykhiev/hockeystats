import makeRequest from 'Api/request';

export default {
  getCurrentSeason() {
    return makeRequest({path: ['season', 'current']});
  }
};
