import Vue from 'vue';
import App from 'Components/App';
import i18n from 'Root/locales';
import router from 'Root/router';
import store from 'Store/store';
import {logger, DEBUG} from 'Root/logger';
import VueGoodTable from 'vue-good-table';
import Tab from 'Components/Tab';
import Tabs from 'Components/Tabs';
import SeasonPicker from 'Components/SeasonPicker';
import StatsBlock from 'Components/StatsBlock';
import TeamsStatsTable from 'Components/TeamsStatsTable';
import SkatersStatsTable from 'Components/SkatersStatsTable';
import GoaliesStatsTable from 'Components/GoaliesStatsTable';
import PlayerMainStat from 'Components/PlayerMainStat';
import PlayerPersonalInfo from 'Components/PlayerPersonalInfo';
import BarChart from 'Components/BarChart';
import StackedBarChart from 'Components/StackedBarChart';

// 3rd party CSS modules
require('../node_modules/normalize.css/normalize.css');
// My CSS
require('../styles/styles.less');

logger.info('App started.');
if (window.location.search.slice(1, 6) === 'debug') {
  logger.setLogLevel(DEBUG);
}

Vue.use(VueGoodTable);
Vue.component('tab', Tab);
Vue.component('tabs', Tabs);
Vue.component('season-picker', SeasonPicker);
Vue.component('stats-block', StatsBlock);
Vue.component('teams-stats-table', TeamsStatsTable);
Vue.component('skaters-stats-table', SkatersStatsTable);
Vue.component('goalies-stats-table', GoaliesStatsTable);
Vue.component('player-main-stat', PlayerMainStat);
Vue.component('player-personal-info', PlayerPersonalInfo);
Vue.component('bar-chart', BarChart);
Vue.component('stacked-bar-chart', StackedBarChart);

new Vue({
  el: '#app',
  router,
  store,
  i18n,
  render: (h) => h(App)
});
