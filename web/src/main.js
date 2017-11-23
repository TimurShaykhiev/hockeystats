import Vue from 'vue';
import App from 'Components/App';
import i18n from 'Root/locales';
import router from 'Root/router';
import store from 'Store/store';
import {logger, DEBUG} from 'Root/logger';
import ToggleButton from 'vue-js-toggle-button';

require('../styles/styles.less');

logger.info('App started.');
if (window.location.search.slice(1, 6) === 'debug') {
  logger.setLogLevel(DEBUG);
}

Vue.use(ToggleButton);

new Vue({
  el: '#app',
  router,
  store,
  i18n,
  render: (h) => h(App)
});
