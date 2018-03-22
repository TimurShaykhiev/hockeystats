<template>
  <div class="teams-compare container-col">
    <div class="container-row" v-if="teamCaptions">
      <div class="teams-compare__header container-row">
        <img :src="teamCaptions.left.logoUrl" class="teams-compare__header-logo">
        <router-link tag="h1" :to="{name: 'team', params: {id: tid1}}" class="teams-compare__header-name">
          <a class="compare--left">{{teamCaptions.left.name}}</a>
        </router-link>
      </div>
      <div class="teams-compare__header container-row">
        <img :src="teamCaptions.right.logoUrl" class="teams-compare__header-logo">
        <router-link tag="h1" :to="{name: 'team', params: {id: tid2}}" class="teams-compare__header-name">
          <a class="compare--right">{{teamCaptions.right.name}}</a>
        </router-link>
      </div>
    </div>
    <h2 class="teams-compare__season-name">{{seasonName}}</h2>
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
    <div class="teams-compare__charts container-row">
      <radar-chart v-if="chartData.radarChart" v-bind="chartData.chartData"/>
    </div>
    <games-table :games="games" :team1Id="tid1" :team2Id="tid2"/>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import CompUtils from 'Components/utils';
import {NumValue} from 'Components/statValue';
import GamesTable from 'Components/GamesTable';

function getTeamNames(d) {
  return [d.team1.abbr, d.team2.abbr];
}

export default {
  name: 'teams-compare',
  components: {GamesTable},
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
    this.requestTeamsCompare();
  },
  computed: {
    seasonName() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        return CompUtils.seasonToStr(season);
      }
      return '';
    },

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
          name: this.$t('statNames.points'),
          attrName: 'points',
          precision: 0
        }, {
          name: this.$t('statNames.pointPercentage'),
          attrName: 'pointPercentage'
        }, {
          name: this.$t('statNames.pointsPerGame'),
          attrName: 'pointsPerGame'
        }, {
          name: this.$t('statNames.homeWinPercentage'),
          attrName: 'homeWinPercentage'
        }, {
          name: this.$t('statNames.awayWinPercentage'),
          attrName: 'awayWinPercentage'
        }, {
          name: this.$t('statNames.shootoutWinPercentage'),
          attrName: 'shootoutWinPercentage'
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
        }, {
          name: this.$t('statNames.oppShootingPercentage'),
          attrName: 'oppShootingPercentage',
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
        }, {
          name: this.$t('statNames.oppShutouts'),
          attrName: 'oppShutouts',
          precision: 0,
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
    },

    games() {
      let data = this.getTeamsCompare();
      if (data === null) {
        return [];
      }
      return data.games;
    },

    chartData() {
      let data = this.getTeamsCompare();
      if (data === null) {
        return {};
      }
      let selSeason = this.$store.state.season.selectedSeason;
      let getRange = this.$store.getters.getTeamStatRange;
      let axises = [
        CompUtils.getAxis('goalsFor', this.$t('statNames.goalsFor'), getRange, selSeason.current),
        CompUtils.getAxis('goalsAgainst', this.$t('statNames.goalsAgainst'), getRange, selSeason.current),
        CompUtils.getAxis('ppPercentage', this.$t('statNames.ppPercentage'), getRange, selSeason.current),
        CompUtils.getAxis('pkPercentage', this.$t('statNames.pkPercentage'), getRange, selSeason.current),
        CompUtils.getAxis('faceOffWinsPercentage', this.$t('statNames.faceOffWinsPercentage'), getRange,
          selSeason.current)
      ];
      return {
        radarChart: true,
        chartData: {
          homogeneous: false,
          axises: axises,
          legend: [
            {key: data.team1.id, name: data.team1.name},
            {key: data.team2.id, name: data.team2.name}
          ],
          dataSet: [
            CompUtils.seasonStatsToChartData(data.stats1, axises, data.team1.id),
            CompUtils.seasonStatsToChartData(data.stats2, axises, data.team2.id)
          ]
        }
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
    a {
      text-decoration: none;
    }
  }
  .teams-compare__season-name {
    text-align: center;
    margin: 1rem 0;
  }
  .teams-compare__main-stats {
    margin: 2rem;
    flex-wrap: wrap;
  }
  .teams-compare__compare-blocks {
    margin: 2rem;
    flex-wrap: wrap;
  }
  .teams-compare__charts {
    justify-content: center;
    margin: 2rem;
  }
</style>
