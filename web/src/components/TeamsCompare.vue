<template>
  <div class="teams-compare container-col">
    <div class="container-row" v-if="teamCaptions">
      <div class="teams-compare__header container-row">
        <img :src="teamCaptions.left.logoUrl" class="teams-compare__header-logo">
        <h1 class="teams-compare__header-name compare--left">{{teamCaptions.left.name}}</h1>
      </div>
      <div class="teams-compare__header container-row">
        <img :src="teamCaptions.right.logoUrl" class="teams-compare__header-logo">
        <h1 class="teams-compare__header-name compare--right">{{teamCaptions.right.name}}</h1>
      </div>
    </div>
    <div class="teams-compare__main-stats container-row">
      <main-stat-compare v-for="el in mainStats" :key="el.id"  v-bind="el"/>
    </div>
    <div class="teams-compare__compare-blocks container-row">
      <stats-compare-block v-if="overallStats" :caption="overallStats.caption" :items="overallStats.stats"/>
      <stats-compare-block v-if="offenceStats" :caption="offenceStats.caption" :items="offenceStats.stats"/>
      <stats-compare-block v-if="defenceStats" :caption="defenceStats.caption" :items="defenceStats.stats"/>
      <stats-compare-block v-if="goalieStats" :caption="goalieStats.caption" :items="goalieStats.stats"/>
      <stats-compare-block v-if="homeStats" :caption="homeStats.caption" :items="homeStats.stats"/>
      <stats-compare-block v-if="awayStats" :caption="awayStats.caption" :items="awayStats.stats"/>
      <stats-compare-block v-if="vsStats" :caption="vsStats.caption" :items="vsStats.stats"/>
    </div>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import CompUtils from 'Components/utils';
import {NumValue} from 'Components/statValue';

function getTeamNames(d) {
  return [d.team1.abbr, d.team2.abbr];
}

export default {
  name: 'teams-compare',
  i18n: {
    messages: {
      en: {
        teamsCompare: {
          overallStatistics: 'OVERALL',
          offenceStatistics: 'OFFENCE',
          defenceStatistics: 'DEFENCE',
          goalieStatistics: 'GOALIE',
          homeStatistics: 'HOME GAMES',
          awayStatistics: 'AWAY GAMES',
          vsStatistics: 'HEAD-TO-HEAD'
        }
      },
      ru: {
        teamsCompare: {
          overallStatistics: 'ОБЩИЕ',
          offenceStatistics: 'НАПАДЕНИЕ',
          defenceStatistics: 'ЗАЩИТА',
          goalieStatistics: 'ВРАТАРИ',
          homeStatistics: 'ДОМАШНИЕ ИГРЫ',
          awayStatistics: 'ГОСТЕВЫЕ ИГРЫ',
          vsStatistics: 'ЛИЧНЫЕ ВСТРЕЧИ'
        }
      }
    }
  },
  data() {
    return {
      tid1: parseInt(this.$route.params.id1),
      tid2: parseInt(this.$route.params.id2)
    };
  },
  created() {
    // debug only
    let season = {regular: true, start: '2017-10-04', current: true, end: '2018-06-30', id: 5, year: 2017};
    this.$store.commit('setSelectedSeason', season);
    // debug only
    this.requestTeamsCompare();
  },
  computed: {
    teamCaptions() {
      let data = this.getTeamsCompare();
      if (data === null) {
        return undefined;
      }
      return {
        left: {logoUrl: `images/team${data.team1.id}.svg`, name: data.team1.name},
        right: {logoUrl: `images/team${data.team2.id}.svg`, name: data.team2.name}
      };
    },

    mainStats() {
      let data = this.getTeamsCompare();
      if (data === null) {
        return [];
      }
      return [
        CompUtils.createMainStatCompare(data, 'goalsForPerGame', 'goalsForPerGameRate',
          this.$t('statNames.goalsForPerGame'), getTeamNames),
        CompUtils.createMainStatCompare(data, 'goalsAgainstPerGame', 'goalsAgainstPerGameRate',
          this.$t('statNames.goalsAgainstPerGame'), getTeamNames, 2, 'asc'),
        CompUtils.createMainStatCompare(data, 'ppPercentage', 'ppPercentageRate',
          this.$t('statNames.ppPercentage'), getTeamNames),
        CompUtils.createMainStatCompare(data, 'pkPercentage', 'pkPercentageRate',
          this.$t('statNames.pkPercentage'), getTeamNames),
        CompUtils.createMainStatCompare(data, 'shootingPercentage', 'shootingPercentageRate',
          this.$t('statNames.shootingPercentage'), getTeamNames)
      ];
    },

    overallStats() {
      let data = this.getTeamsCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('teamsCompare.overallStatistics'), getTeamNames, [{
          name: this.$t('statNames.pointPercentage'),
          attrName: 'pointPercentage'
        }, {
          name: this.$t('statNames.pointsPerGame'),
          attrName: 'pointsPerGame'
        }, {
          name: this.$t('statNames.faceOffWinsPercentage'),
          attrName: 'faceOffWinsPercentage'
        }]
      );
    },

    offenceStats() {
      let data = this.getTeamsCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('teamsCompare.offenceStatistics'), getTeamNames, [{
          name: this.$t('statNames.goalsFor'),
          attrName: 'goalsFor',
          precision: 0
        }, {
          name: this.$t('statNames.ppGoals'),
          attrName: 'ppGoals',
          precision: 0
        }, {
          name: this.$t('statNames.ppPercentage'),
          attrName: 'ppPercentage'
        }, {
          name: this.$t('statNames.shootingPercentage'),
          attrName: 'shootingPercentage'
        }, {
          name: this.$t('statNames.goalsForPerGame'),
          attrName: 'goalsForPerGame'
        }, {
          name: this.$t('statNames.shotsPerGame'),
          attrName: 'shotsPerGame'
        }, {
          name: this.$t('statNames.ppGoalsPerGame'),
          attrName: 'ppGoalsPerGame'
        }, {
          name: this.$t('statNames.ppPerGame'),
          attrName: 'ppPerGame'
        }]
      );
    },

    defenceStats() {
      let data = this.getTeamsCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('teamsCompare.defenceStatistics'), getTeamNames, [{
          name: this.$t('statNames.goalsAgainst'),
          attrName: 'goalsAgainst',
          precision: 0,
          order: 'asc'
        }, {
          name: this.$t('statNames.shGoalsAgainst'),
          attrName: 'shGoalsAgainst',
          precision: 0,
          order: 'asc'
        }, {
          name: this.$t('statNames.pkPercentage'),
          attrName: 'pkPercentage'
        }, {
          name: this.$t('statNames.goalsAgainstPerGame'),
          attrName: 'goalsAgainstPerGame',
          order: 'asc'
        }, {
          name: this.$t('statNames.shotsAgainstPerGame'),
          attrName: 'shotsAgainstPerGame',
          order: 'asc'
        }, {
          name: this.$t('statNames.shGoalsAgainstPerGame'),
          attrName: 'shGoalsAgainstPerGame',
          order: 'asc'
        }, {
          name: this.$t('statNames.shPerGame'),
          attrName: 'shPerGame',
          order: 'asc'
        }]
      );
    },

    goalieStats() {
      let data = this.getTeamsCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('teamsCompare.goalieStatistics'), getTeamNames, [{
          name: this.$t('statNames.savePercentage'),
          attrName: 'savePercentage',
          precision: 3
        }, {
          name: this.$t('statNames.shutouts'),
          attrName: 'shutouts',
          precision: 0
        }, {
          name: this.$t('statNames.oppSavePercentage'),
          attrName: 'oppSavePercentage',
          precision: 3,
          order: 'asc'
        }]
      );
    },

    homeStats() {
      let data = this.getTeamsCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('teamsCompare.homeStatistics'), getTeamNames, [{
          name: this.$t('statNames.goalsFor'),
          attrName: 'homeGoals',
          precision: 0
        }, {
          name: this.$t('statNames.goalsAgainst'),
          attrName: 'homeGoalsAgainst',
          precision: 0,
          order: 'asc'
        }, {
          name: this.$t('statNames.shots'),
          attrName: 'homeShots',
          precision: 0
        }, {
          name: this.$t('statNames.shotsAgainst'),
          attrName: 'homeShotsAgainst',
          precision: 0,
          order: 'asc'
        }, {
          name: this.$t('statNames.ppPercentage'),
          attrName: 'homePPPercentage'
        }, {
          name: this.$t('statNames.pkPercentage'),
          attrName: 'homePKPercentage'
        }]
      );
    },

    awayStats() {
      let data = this.getTeamsCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('teamsCompare.awayStatistics'), getTeamNames, [{
          name: this.$t('statNames.goalsFor'),
          attrName: 'awayGoals',
          precision: 0
        }, {
          name: this.$t('statNames.goalsAgainst'),
          attrName: 'awayGoalsAgainst',
          precision: 0,
          order: 'asc'
        }, {
          name: this.$t('statNames.shots'),
          attrName: 'awayShots',
          precision: 0
        }, {
          name: this.$t('statNames.shotsAgainst'),
          attrName: 'awayShotsAgainst',
          precision: 0,
          order: 'asc'
        }, {
          name: this.$t('statNames.ppPercentage'),
          attrName: 'awayPPPercentage'
        }, {
          name: this.$t('statNames.pkPercentage'),
          attrName: 'awayPKPercentage'
        }]
      );
    },

    vsStats() {
      let data = this.getTeamsCompare();
      if (data === null) {
        return undefined;
      }

      function createVsStats(fields) {
        return fields.map((el) => ({
          name: el.name,
          lValue: new NumValue(data.vs[`${el.attrName}1`], el.precision),
          rValue: new NumValue(data.vs[`${el.attrName}2`], el.precision),
          sortOrder: el.order || 'desc'
        }));
      }

      let [lName, rName] = getTeamNames(data);
      return {
        caption: {title: this.$t('teamsCompare.vsStatistics'), lName: lName, rName: rName},
        stats: createVsStats([{
            name: this.$t('statNames.goalsFor'),
            attrName: 'goals',
            precision: 0
          }, {
            name: this.$t('statNames.shots'),
            attrName: 'shots',
            precision: 0
          }, {
            name: this.$t('statNames.ppPercentage'),
            attrName: 'ppp'
          }, {
            name: this.$t('statNames.pkPercentage'),
            attrName: 'pkp'
          }, {
            name: this.$t('statNames.penaltyMinutes'),
            attrName: 'pim',
            precision: 0,
            order: 'asc'
          }])
      };
    }
  },
  methods: {
    requestTeamsCompare() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getTeamsComparison', {
          id1: this.tid1,
          id2: this.tid2,
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    },

    getTeamsCompare() {
      let season = this.$store.state.season.selectedSeason;
      let data = this.$store.getters.getTeamsComparison(season, this.tid1, this.tid2);
      if (data === null) {
        this.requestTeamsCompare();
      }
      return data;
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .teams-compare__header {
    align-items: center;
    padding: 0 1rem;
    flex: 1;
  }
  .teams-compare__header-logo {
    width: 8rem;
    height: 8rem;
    flex: 1;
  }
  .teams-compare__header-name {
    font-size: 2.5rem;
    padding-left: 1.5rem;
    flex: 4;
  }
  .teams-compare__main-stats {
    margin: 2rem;
    flex-wrap: wrap;
  }
  .teams-compare__compare-blocks {
    margin: 2rem;
    flex-wrap: wrap;
  }
</style>
