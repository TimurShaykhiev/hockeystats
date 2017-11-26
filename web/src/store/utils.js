export function commitNew(commit, mutName, state, newState) {
  if (state && state.timestamp !== newState.timestamp) {
    commit(mutName, newState);
  }
}

export function getPercentage(value, total, raw=false) {
  let p = 0;
  if (total > 0) {
    p = (raw ? value : (value * 100)) / total;
  }
  return p;
}
