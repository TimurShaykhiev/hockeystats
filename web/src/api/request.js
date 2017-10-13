import 'whatwg-fetch';

const API_URL = 'http://localhost:5000/api/v1/';

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min)) + min;
}

const result = {
  season: {year: 2017, regular: true},
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

export function getData(url) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      resolve(result);
    }, 100);
  });
}
