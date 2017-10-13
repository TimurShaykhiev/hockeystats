import {getData, buildUrl} from 'Api/request';

export default {
  getSkatersStats(reqParams) {
    let urlData = {
      path: ['stats', 'skaters'],
      query: reqParams.getQueryParams()
    };
    return getData(buildUrl(urlData));
  }
};
