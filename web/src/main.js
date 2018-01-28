import Vue from 'vue';
import App from 'Components/App';
import i18n from 'Root/locales';
import router from 'Root/router';
import store from 'Store/store';
import {logger, DEBUG} from 'Root/logger';
import VueGoodTable from 'vue-good-table';
import Tab from 'Components/Tab';
import Tabs from 'Components/Tabs';

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

new Vue({
  el: '#app',
  router,
  store,
  i18n,
  render: (h) => h(App)
});
