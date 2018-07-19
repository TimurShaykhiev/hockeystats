import makeRequest from 'Api/request';

export default {
  getScorerDuos(reqParams) {
    let reqData = {
      path: ['ratings', 'scorer-duos'],
      query: reqParams.getQueryParams()
    };
    return makeRequest(reqData);
  }
};
