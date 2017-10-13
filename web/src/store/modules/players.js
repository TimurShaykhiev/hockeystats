import players from 'Api/players';

const state = {
  skaterStats: {}
};

const getters = {
};

const actions = {
  getSkatersStats({commit, state}, {reqParams}) {
    players.getSkatersStats(reqParams)
      .then((data) => {
        commit('setSkaterStats', {stats: data});
      });
  }
};

const mutations = {
  setSkaterStats(state, {stats}) {
    let newStat = {};
    newStat.season = stats.season;
    newStat.skaters = [];
    for (let s of stats.results) {
      let skater = {player: s.player, stats: {}};
      skater.stats.goals = s.stats[0];
      skater.stats.assists = s.stats[1];
      skater.stats.plusMinus = s.stats[2];
      skater.stats.toi = s.stats[3];
      newStat.skaters.push(skater);
    }
    state.skaterStats = newStat;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
