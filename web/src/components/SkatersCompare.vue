<template>
  <div class="skaters-compare container-col">
    <div class="container-row" v-if="playersInfo">
      <div class="skaters-compare__header container-row">
        <player-personal-info :playerInfo="playersInfo.left" :fullWidth="false" comparePosition="left"/>
      </div>
      <div class="skaters-compare__header container-row">
        <player-personal-info :playerInfo="playersInfo.right" :fullWidth="false" comparePosition="right"/>
      </div>
    </div>
    <h2 class="skaters-compare__season-name">{{seasonName}}</h2>
    <div class="skaters-compare__main-stats container-row">
      <main-stat-compare v-for="el in mainStats" :key="el.id"  v-bind="el"/>
    </div>
    <div class="skaters-compare__compare-blocks container-row">
      <stats-compare-block v-if="overallStats" :caption="overallStats.caption" :items="overallStats.stats"/>
      <stats-compare-block v-if="offenceStats" :caption="offenceStats.caption" :items="offenceStats.stats"/>
      <stats-compare-block v-if="defenceStats" :caption="defenceStats.caption" :items="defenceStats.stats"/>
      <stats-compare-block v-if="homeStats" :caption="homeStats.caption" :items="homeStats.stats"/>
      <stats-compare-block v-if="awayStats" :caption="awayStats.caption" :items="awayStats.stats"/>
    </div>
    <div class="skaters-compare__charts container-row">
      <radar-chart v-if="chartData.radarChart" v-bind="chartData.chartData"/>
    </div>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import CompUtils from 'Components/utils';

export default {
  name: 'skaters-compare',
  i18n: {
    messages: {
      en: {
        skatersCompare: {
          overallStatistics: 'OVERALL',
          offenceStatistics: 'OFFENCE',
          defenceStatistics: 'DEFENCE',
          homeStatistics: 'HOME GAMES',
          awayStatistics: 'AWAY GAMES'
        }
      },
      ru: {
        skatersCompare: {
          overallStatistics: 'ОБЩИЕ',
          offenceStatistics: 'НАПАДЕНИЕ',
          defenceStatistics: 'ЗАЩИТА',
          homeStatistics: 'ДОМАШНИЕ ИГРЫ',
          awayStatistics: 'ГОСТЕВЫЕ ИГРЫ'
        }
      }
    }
  },
  data() {
    return {
      pid1: parseInt(this.$route.params.id1),
      pid2: parseInt(this.$route.params.id2)
    };
  },
  created() {
    this.requestSkatersCompare();
  },
  computed: {
    seasonName() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        return CompUtils.seasonToStr(season);
      }
      return '';
    },

    playersInfo() {
      let data = this.getSkatersCompare();
      if (data === null) {
        return undefined;
      }
      return {
        left: data.player1,
        right: data.player2
      };
    },

    mainStats() {
      let data = this.getSkatersCompare();
      if (data === null) {
        return [];
      }
      return [
        CompUtils.createMainStatCompare(data, 'goals', 'goalsRateTotal', this.$t('statNames.goals'),
          CompUtils.getPlayerShortNames, 0),
        CompUtils.createMainStatCompare(data, 'assists', 'assistsRateTotal', this.$t('statNames.assists'),
          CompUtils.getPlayerShortNames, 0),
        CompUtils.createMainStatCompare(data, 'points', 'pointsRateTotal', this.$t('statNames.points'),
          CompUtils.getPlayerShortNames, 0),
        CompUtils.createMainStatCompare(data, 'plusMinus', 'plusMinusRateTotal', this.$t('statNames.plusMinus'),
          CompUtils.getPlayerShortNames, 0),
        CompUtils.createMainStatCompare(data, 'turnover', 'turnoverRateTotal', this.$t('statNames.turnover'),
          CompUtils.getPlayerShortNames, 0)
      ];
    },

    overallStats() {
      let data = this.getSkatersCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('skatersCompare.overallStatistics'),
        CompUtils.getPlayerShortNames, [{
          name: this.$t('statNames.points'),
          attrName: 'points',
          precision: 0
        }, {
          name: this.$t('statNames.plusMinus'),
          attrName: 'plusMinus',
          precision: 0
        }, {
          name: this.$t('statNames.toiPerGame'),
          attrName: 'toiPerGame',
          time: true
        }, {
          name: this.$t('statNames.faceOffWinsPercentage'),
          attrName: 'faceOffWinsPercentage'
        }, {
          name: this.$t('statNames.penaltyMinutes'),
          attrName: 'penaltyMinutes',
          precision: 0,
          order: 'asc'
        }]
      );
    },

    offenceStats() {
      let data = this.getSkatersCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('skatersCompare.offenceStatistics'),
        CompUtils.getPlayerShortNames, [{
          name: this.$t('statNames.goals'),
          attrName: 'goals',
          precision: 0
        }, {
          name: this.$t('statNames.assists'),
          attrName: 'assists',
          precision: 0
        }, {
          name: this.$t('statNames.shots'),
          attrName: 'shots',
          precision: 0
        }, {
          name: this.$t('statNames.shootingPercentage'),
          attrName: 'shootingPercentage'
        }, {
          name: this.$t('statNames.goalsPer60min'),
          attrName: 'goalsPer60min',
          precision: 1
        }, {
          name: this.$t('statNames.shotsPer60min'),
          attrName: 'shotsPer60min',
          precision: 1
        }]
      );
    },

    defenceStats() {
      let data = this.getSkatersCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('skatersCompare.defenceStatistics'),
        CompUtils.getPlayerShortNames, [{
          name: this.$t('statNames.turnover'),
          attrName: 'turnover',
          precision: 0
        }, {
          name: this.$t('statNames.turnoverPer60min'),
          attrName: 'turnoverPer60min',
          precision: 1
        }, {
          name: this.$t('statNames.hits'),
          attrName: 'hits',
          precision: 0
        }, {
          name: this.$t('statNames.hitsPer60min'),
          attrName: 'hitsPer60min',
          precision: 1
        }, {
          name: this.$t('statNames.blocks'),
          attrName: 'blocks',
          precision: 0
        }, {
          name: this.$t('statNames.blocksPer60min'),
          attrName: 'blocksPer60min',
          precision: 1
        }]
      );
    },

    homeStats() {
      let data = this.getSkatersCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('skatersCompare.homeStatistics'),
        CompUtils.getPlayerShortNames, [{
          name: this.$t('statNames.goals'),
          attrName: 'homeGoals',
          precision: 0
        }, {
          name: this.$t('statNames.assists'),
          attrName: 'homeAssists',
          precision: 0
        }, {
          name: this.$t('statNames.plusMinus'),
          attrName: 'homePlusMinus',
          precision: 0
        }, {
          name: this.$t('statNames.turnover'),
          attrName: 'homeTurnover',
          precision: 0
        }, {
          name: this.$t('statNames.pointsPerGame'),
          attrName: 'homePointsPerGame',
          precision: 1
        }, {
          name: this.$t('statNames.penaltyMinutes'),
          attrName: 'homePim',
          precision: 0,
          order: 'asc'
        }]
      );
    },

    awayStats() {
      let data = this.getSkatersCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('skatersCompare.awayStatistics'),
        CompUtils.getPlayerShortNames, [{
          name: this.$t('statNames.goals'),
          attrName: 'awayGoals',
          precision: 0
        }, {
          name: this.$t('statNames.assists'),
          attrName: 'awayAssists',
          precision: 0
        }, {
          name: this.$t('statNames.plusMinus'),
          attrName: 'awayPlusMinus',
          precision: 0
        }, {
          name: this.$t('statNames.turnover'),
          attrName: 'awayTurnover',
          precision: 0
        }, {
          name: this.$t('statNames.pointsPerGame'),
          attrName: 'awayPointsPerGame',
          precision: 1
        }, {
          name: this.$t('statNames.penaltyMinutes'),
          attrName: 'awayPim',
          precision: 0,
          order: 'asc'
        }]
      );
    },

    chartData() {
      let data = this.getSkatersCompare();
      if (data === null) {
        return {};
      }
      let selSeason = this.$store.state.season.selectedSeason;
       let getRange = this.$store.getters.getSkaterStatRange;
       let axises = [
         CompUtils.getAxis('goals', this.$t('statNames.goals'), getRange, selSeason.current),
         CompUtils.getAxis('assists', this.$t('statNames.assists'), getRange, selSeason.current),
         CompUtils.getAxis('plusMinus', this.$t('statNames.plusMinus'), getRange, selSeason.current),
         CompUtils.getAxis('turnover', this.$t('statNames.turnover'), getRange, selSeason.current),
         CompUtils.getAxis('penaltyMinutes', this.$t('statNames.penaltyMinutes'), getRange, selSeason.current)
       ];
      return {
        radarChart: true,
        chartData: {
          homogeneous: false,
          axises: axises,
          legend: [
            {key: data.player1.id, name: data.player1.name},
            {key: data.player2.id, name: data.player2.name}
          ],
          dataSet: [
            CompUtils.seasonStatsToChartData(data.stats1, axises, data.player1.id),
            CompUtils.seasonStatsToChartData(data.stats2, axises, data.player2.id)
          ]
        }
      };
    }
  },
  methods: {
    requestSkatersCompare() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getSkatersComparison', {
          id1: this.pid1,
          id2: this.pid2,
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    },

    getSkatersCompare() {
      let season = this.$store.state.season.selectedSeason;
      let data = this.$store.getters.getSkatersComparison(season, this.pid1, this.pid2);
      if (data === null) {
        this.requestSkatersCompare();
      }
      return data;
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .skaters-compare__header {
    align-items: center;
    padding: 0 1rem;
    flex: 1;
  }
  .skaters-compare__season-name {
    text-align: center;
    margin: 1rem 0;
  }
  .skaters-compare__main-stats {
    margin: 2rem;
    flex-wrap: wrap;
  }
  .skaters-compare__compare-blocks {
    margin: 2rem;
    flex-wrap: wrap;
  }
  .skaters-compare__charts {
    justify-content: center;
    margin: 2rem;
  }
</style>
