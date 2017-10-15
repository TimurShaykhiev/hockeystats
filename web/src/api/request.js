import 'whatwg-fetch';
import ApiErrors from 'Api/apiErrors';

const API_URL = 'http://localhost:5000/api/v1/';

let pendingStates = {};

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;
}

const result = {
  season: {year: 2017, regular: true, current: true},
  results: [
    {player: {id: 1, name: 'Alex Ovechkin', team: 'WSH'}, stats: Array.from(new Array(20), () => getRandomInt(0, 10))},
    {player: {id: 2, name: 'Sydney Crosby', team: 'PTB'}, stats: Array.from(new Array(20), () => getRandomInt(0, 10))},
    {player: {id: 3, name: 'Phil Kessel', team: 'PTB'}, stats: Array.from(new Array(20), () => getRandomInt(0, 10))},
    {player: {id: 4, name: 'Connor McDavid', team: 'EDM'}, stats: Array.from(new Array(20), () => getRandomInt(0, 10))},
    {player: {id: 5, name: 'Joe Tornton', team: 'SJS'}, stats: Array.from(new Array(20), () => getRandomInt(0, 10))},
    {player: {id: 6, name: 'Nikita Kucherov', team: 'TBL'}, stats: Array.from(new Array(20), () => getRandomInt(0, 10))}
  ]
};

// URL data has format:
// - path - array of path elements.
// - query - array of {name, value, required}. 'required' can be omitted.
export function buildUrl(data) {
  let path = data.path.join('/');
  let query = [];
  for (let q of data.query) {
    if (q.value !== null) {
      query.push(`${q.name}=${encodeURIComponent(q.value)}`);
    } else if (q.required) {
      throw new Error(`Required query parameter ${q.name} is missed.`);
    }
  }
  if (query.length > 0) {
    return `${API_URL}${path}?${query.join('&')}`;
  }
  return `${API_URL}${path}`;
}

export function makeRequest(url) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve(result);
      // reject(new Error('NetworkError'));
    }, getRandomInt(100, 300));
  });
}

// This function also checks do we have pending request of the same type.
export function makeRequestIfNeeded(pendingStateName, prepareRequestData) {
  if (pendingStates[pendingStateName] === true) {
    // request is already in progress
    return Promise.reject(new Error(ApiErrors.DUPLICATE_REQUEST));
  }

  let reqData = prepareRequestData();
  pendingStates[pendingStateName] = true;

  return makeRequest(buildUrl(reqData)).then(
    (result) => {
      pendingStates[pendingStateName] = false;
      return result;
    },
    (error) => {
      pendingStates[pendingStateName] = false;
      throw error;
    }
  );
}
