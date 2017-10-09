import Vue from 'vue';
import VueI18n from 'vue-i18n';
import VueRouter from 'vue-router';
import App from 'Components/App';
import locales from 'Root/locales';
import routes from 'Root/routes';
import UserSettings from 'Root/userSettings';

require('../styles/styles.less');

Vue.use(VueI18n);
Vue.use(VueRouter);

const settings = new UserSettings();

locales.locale = settings.locale;
const i18n = new VueI18n(locales);

const router = new VueRouter({
  routes
});

new Vue({
  el: '#app',
  router,
  i18n,
  render: (h) => h(App)
});
