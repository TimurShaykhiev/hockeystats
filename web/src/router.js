import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from 'Components/Home';
import Teams from 'Components/Teams';
import Players from 'Components/Players';

Vue.use(VueRouter);

const routes = [{
    path: '/teams',
    name: 'teams',
    component: Teams
  }, {
    path: '/players',
    name: 'players',
    component: Players
  }, {
    path: '/',
    name: 'home',
    component: Home
  }
];

export default new VueRouter({
  routes
});
