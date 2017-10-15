import {makeRequestIfNeeded} from 'Api/request';

export default {
  getSkaterStats(reqParams) {
    return makeRequestIfNeeded('skaterStats', () => {
      return {
        path: ['stats', 'skaters'],
        query: reqParams.getQueryParams()
      };
    });
  },

  getGoalieStats(reqParams) {
    return makeRequestIfNeeded('goalieStats', () => {
      return {
        path: ['stats', 'goalies'],
        query: reqParams.getQueryParams()
      };
    });
  }
};
