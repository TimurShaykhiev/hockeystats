import {logger} from 'Root/logger';

export function commitNew(commit, mutName, state, newState) {
  if (state && state.timestamp !== newState.timestamp) {
    commit(mutName, newState);
  }
}

export function processRequest(actName, mutName, stateName, commit, state, requestPromise) {
  return requestPromise.then(
      (result) => {
        logger.debug(`action: ${actName} result received`);
        commitNew(commit, mutName, state[stateName], result);
        return state[stateName];
      },
      (error) => {
        logger.error(`action: ${actName} error: ${error.message}`);
      }
    );
}

export function skaterStatsArrayToObject(statsArray) {
  let obj = {
    assists: statsArray[0],
    goals: statsArray[1],
    shots: statsArray[2],
    ppGoals: statsArray[3],
    penaltyMinutes: statsArray[4],
    shGoals: statsArray[5],
    plusMinus: statsArray[6],
    games: statsArray[7],
    points: statsArray[8],
    ppPoints: statsArray[9],
    shPoints: statsArray[10],
    faceOffTaken: statsArray[11],
    pointsPerGame: statsArray[12],
    toiPerGame: statsArray[13],
    shootingPercentage: statsArray[14],
    faceOffWinsPercentage: statsArray[15]
  };
  obj.evenGoals = obj.goals - obj.ppGoals - obj.shGoals;
  obj.evenPoints = obj.points - obj.ppPoints - obj.shPoints;
  obj.ppAssists = obj.ppPoints - obj.ppGoals;
  obj.shAssists = obj.shPoints - obj.shGoals;
  obj.evenAssists = obj.assists - obj.ppAssists - obj.shAssists;
  return obj;
}

export function goalieStatsArrayToObject(statsArray) {
  return {
    toi: statsArray[0],
    assists: statsArray[1],
    goals: statsArray[2],
    penaltyMinutes: statsArray[3],
    shots: statsArray[4],
    saves: statsArray[5],
    games: statsArray[6],
    wins: statsArray[7],
    shutout: statsArray[8],
    points: statsArray[9],
    losses: statsArray[10],
    goalsAgainst: statsArray[11],
    gaa: statsArray[12],
    svp: statsArray[13]
  };
}

export function isCorrectSeason(season, stats) {
  return stats.season && season.id && season.id === stats.season.id && season.regular === stats.season.regular;
}
