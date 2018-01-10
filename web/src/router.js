import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from 'Components/Home';
import Teams from 'Components/Teams';
import Skaters from 'Components/Skaters';
import Goalies from 'Components/Goalies';
import TeamInfo from 'Components/TeamInfo';
import SkaterInfo from 'Components/SkaterInfo';
import GoalieInfo from 'Components/GoalieInfo';

Vue.use(VueRouter);

const routes = [{
    path: '/team/:id',
    name: 'team',
    component: TeamInfo
  }, {
    path: '/skater/:id',
    name: 'skater',
    component: SkaterInfo
  }, {
    path: '/goalie/:id',
    name: 'goalie',
    component: GoalieInfo
  }, {
    path: '/teams',
    name: 'teams',
    component: Teams
  }, {
    path: '/skaters',
    name: 'skaters',
    component: Skaters
  }, {
    path: '/goalies',
    name: 'goalies',
    component: Goalies
  }, {
    path: '/',
    name: 'home',
    component: Home
  }
];

export default new VueRouter({
  routes
});
