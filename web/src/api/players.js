import {makeRequestIfNeeded} from 'Api/request';

export default {
  getSkatersStats(reqParams) {
    return makeRequestIfNeeded('skaterStats', () => {
      return {
        path: ['stats', 'skaters'],
        query: reqParams.getQueryParams()
      };
    });
  }
};
