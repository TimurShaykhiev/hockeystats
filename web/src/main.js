import Vue from 'vue';
import App from 'Components/App';

require('../styles/styles.less');

new Vue({
  el: '#app',
  render: (h) => h(App)
});
