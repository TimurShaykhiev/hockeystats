import Vue from 'vue';
import VueI18n from 'vue-i18n';
import App from 'Components/App';
import locales from 'Root/locales';
import UserSettings from 'Root/userSettings';

require('../styles/styles.less');

Vue.use(VueI18n);

const settings = new UserSettings();
locales.locale = settings.locale;
const i18n = new VueI18n(locales);

new Vue({
  el: '#app',
  i18n,
  render: (h) => h(App)
});
