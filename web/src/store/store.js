import Vue from 'vue';
import Vuex from 'vuex';
import teams from 'Store/modules/teams';
import players from 'Store/modules/players';
import season from 'Store/modules/season';
import ratings from 'Store/modules/ratings';
import UserSettings from 'Root/userSettings';

Vue.use(Vuex);

const settings = new UserSettings();

export default new Vuex.Store({
  state: {
    userLocale: settings.locale
  },
  modules: {
    teams,
    players,
    season,
    ratings
  }
});
