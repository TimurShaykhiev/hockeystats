export function commitNew(commit, mutName, state, newState) {
  if (state && state.timestamp !== newState.timestamp) {
    commit(mutName, newState);
  }
}
