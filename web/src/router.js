import Vue from 'vue';
import VueRouter from 'vue-router';
import i18n from 'Root/locales';
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
    component: TeamInfo,
    meta: {
      title: i18n.t('pageTitle.teamInfo')
    }
  }, {
    path: '/skater/:id',
    name: 'skater',
    component: SkaterInfo,
    meta: {
      title: i18n.t('pageTitle.skaterInfo')
    }
  }, {
    path: '/goalie/:id',
    name: 'goalie',
    component: GoalieInfo,
    meta: {
      title: i18n.t('pageTitle.goalieInfo')
    }
  }, {
    path: '/teams/compare/:id1/:id2',
    name: 'teamsCompare',
    component: TeamsCompare,
    meta: {
      title: i18n.t('pageTitle.teamsCompare')
    }
  }, {
    path: '/teams',
    name: 'teams',
    component: Teams,
    meta: {
      title: i18n.t('pageTitle.teams')
    }
  }, {
    path: '/skaters/compare/:id1/:id2',
    name: 'skatersCompare',
    component: SkatersCompare,
    meta: {
      title: i18n.t('pageTitle.skatersCompare')
    }
  }, {
    path: '/skaters',
    name: 'skaters',
    component: Skaters,
    meta: {
      title: i18n.t('pageTitle.skaters')
    }
  }, {
    path: '/goalies/compare/:id1/:id2',
    name: 'goaliesCompare',
    component: GoaliesCompare,
    meta: {
      title: i18n.t('pageTitle.goaliesCompare')
    }
  }, {
    path: '/goalies',
    name: 'goalies',
    component: Goalies,
    meta: {
      title: i18n.t('pageTitle.goalies')
    }
  }, {
    path: '/compare',
    name: 'compare',
    component: Compare,
    meta: {
      title: i18n.t('pageTitle.compare')
    }
  }, {
    path: '/',
    name: 'home',
    component: Home,
    meta: {
      title: i18n.t('pageTitle.home')
    }
  }
];

const router = new VueRouter({
  routes
});

router.beforeEach((to, from, next) => {
  document.title = to.meta.title;
  next();
});

export default router;
