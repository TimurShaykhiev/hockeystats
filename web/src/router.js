import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from 'Components/Home';
import Teams from 'Components/Teams';
import Skaters from 'Components/Skaters';
import Goalies from 'Components/Goalies';
import TeamInfo from 'Components/TeamInfo';
import SkaterInfo from 'Components/SkaterInfo';
import GoalieInfo from 'Components/GoalieInfo';
import Compare from 'Components/Compare';
import TeamsCompare from 'Components/TeamsCompare';
import SkatersCompare from 'Components/SkatersCompare';
import GoaliesCompare from 'Components/GoaliesCompare';

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
    path: '/teams/compare/:id1/:id2',
    name: 'teamsCompare',
    component: TeamsCompare
  }, {
    path: '/teams',
    name: 'teams',
    component: Teams
  }, {
    path: '/skaters/compare/:id1/:id2',
    name: 'skatersCompare',
    component: SkatersCompare
  }, {
    path: '/skaters',
    name: 'skaters',
    component: Skaters
  }, {
    path: '/goalies/compare/:id1/:id2',
    name: 'goaliesCompare',
    component: GoaliesCompare
  }, {
    path: '/goalies',
    name: 'goalies',
    component: Goalies
  }, {
    path: '/compare',
    name: 'compare',
    component: Compare
  }, {
    path: '/',
    name: 'home',
    component: Home
  }
];

export default new VueRouter({
  routes
});
