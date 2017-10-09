import Home from 'Components/Home';
import Teams from 'Components/Teams';
import Players from 'Components/Players';

export default [{
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
