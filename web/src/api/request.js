import 'whatwg-fetch';
import ApiErrors from 'Api/apiErrors';
import {logger} from 'Root/logger';

// const API_URL = 'http://localhost:9000/api/';
const API_URL = 'http://hockeystats.com/api/';

// URL data has format:
// - path - array of path elements.
// - query - array of {name, value, required}. 'required' can be omitted.
function buildUrl(data) {
  let path = data.path.join('/');
  let query = [];
  if (data.query) {
    for (let q of data.query) {
      if (q.value !== null) {
        query.push(`${q.name}=${encodeURIComponent(q.value)}`);
      } else if (q.required) {
        throw new Error(`Required query parameter ${q.name} is missed.`);
      }
    }
  }
  if (query.length > 0) {
    return `${API_URL}${path}?${query.join('&')}`;
  }
  return `${API_URL}${path}`;
}

class RequestManager {
  constructor() {
    // Dictionary of url:promise.
    this.pendingRequests = {};
  }

  sendRequest(requestData) {
    let url = buildUrl(requestData);
    if (url in this.pendingRequests) {
      // Request is already in progress. Return promise for this request.
      return this.pendingRequests[url];
    }

    let promise = this.fetchData(url);
    this.pendingRequests[url] = promise;

    return promise.then(
      (result) => {
        delete this.pendingRequests[url];
        return result;
      },
      (error) => {
        delete this.pendingRequests[url];
        throw error;
      }
    );
  }

  fetchData(url) {
    return fetch(url)
      .then(
        (response) => {
          if ((response.status >= 200 && response.status < 300) ||
              (response.status >= 400 && response.status < 500)) {
            return response;
          } else {
            let error = new Error(response.statusText);
            error.response = response;
            throw error;
          }
        },
        (error) => {
          logger.error(`Fetch failed ${error}`);
          throw new Error(ApiErrors.FETCH_FAILED);
        })
      .then((response) => response.json())
      .then((response) => {
        if (response.error) {
          // API error. It must contain error code in JSON response.
          throw new Error(response.error);
        }
        response.timestamp = Date.now();
        return response;
      });
  }
}

let requestManager = new RequestManager();

export default function makeRequest(requestData) {
  return requestManager.sendRequest(requestData);
}
