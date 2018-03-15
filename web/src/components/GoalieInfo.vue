<template>
  <div class="goalie-info container-col">
    <player-personal-info :playerInfo="playerInfo" v-if="playerInfo.id"/>
    <div class="goalie-info__selectors container-row">
      <item-selector class="goalie-info__selector" type="goalie"/>
      <season-picker class="goalie-info__season-picker" type="goalie"/>
    </div>
    <div class="container-row">
      <player-main-stat v-for="el in ratings" :key="el.id" v-bind="el"/>
    </div>
    <tabs>
      <tab :name="$t('tabNames.charts')">
        <select class="chart-picker__select" v-model="selectedChart">
          <option v-for="el in chartList" :value="el.value">{{el.name}}</option>
        </select>
        <bar-chart v-if="chartData.barChart" v-bind="chartData.chartData"/>
        <stacked-bar-chart v-else-if="chartData.stackedBarChart" v-bind="chartData.chartData"/>
      </tab>
      <tab :name="$t('tabNames.table')">
        <goalies-stats-table type="player"/>
      </tab>
    </tabs>
    <stats-block :caption="$t('goalieInfo.saveStatistics')" :items="saveStats"/>
    <stats-block :caption="$t('goalieInfo.goalStatistics')" :items="goalStats"/>
    <stats-block :caption="$t('goalieInfo.homeStatistics')" :items="homeStats"/>
    <stats-block :caption="$t('goalieInfo.awayStatistics')" :items="awayStats"/>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import ItemSelector from 'Components/ItemSelector';
import CompUtils from 'Components/utils';
import {format} from 'd3-format';
import {NumValue} from 'Components/statValue';

let f3 = format('.3f');

const CHART_GAA = 1;
const CHART_SP = 2;
const CHART_WINS = 3;
const CHART_SHUTOUTS = 4;
const CHART_TOI = 5;

export default {
  name: 'goalie-info',
  components: {ItemSelector},
  props: {
  },
  i18n: {
    messages: {
      en: {
        goalieInfo: {
          saveStatistics: 'SAVES',
          goalStatistics: 'GOALS',
          homeStatistics: 'HOME STATISTICS',
          awayStatistics: 'AWAY STATISTICS'
        }
      },
      ru: {
        goalieInfo: {
          saveStatistics: 'СПАСЕНИЯ',
          goalStatistics: 'ГОЛЫ',
          homeStatistics: 'СТАТИСТИКА В ДОМАШНИХ ИГРАХ',
          awayStatistics: 'СТАТИСТИКА В ГОСТЕВЫХ ИГРАХ'
        }
      }
    }
  },
  data() {
    return {
      selectedChart: CHART_GAA,
      chartList: [
        {name: this.$t('charts.goalsAgainstAverage'), value: CHART_GAA},
        {name: this.$t('charts.savePercentage'), value: CHART_SP},
        {name: this.$t('charts.wins'), value: CHART_WINS},
        {name: this.$t('charts.shutouts'), value: CHART_SHUTOUTS},
        {name: this.$t('charts.toi'), value: CHART_TOI}
      ]
    };
  },
  created() {
    this.requestGoalieInfo();
  },
  computed: {
    playerInfo() {
      let goalieInfo = this.$store.state.players.goalieSeasonInfo;
      if (!goalieInfo.player) {
        return {};
      }
      return goalieInfo.player;
    },

    ratings() {
      let goalieInfo = this.getGoalieInfo();
      if (goalieInfo === null) {
        return [];
      }
      return [{
        id: 'gaa',
        label: this.$t('statNames.goalsAgainstAverage'),
        value: new NumValue(goalieInfo.gaa),
        rating: new NumValue(goalieInfo.gaaRate)
      }, {
        id: 'svp',
        label: this.$t('statNames.savePercentage'),
        value: new NumValue(goalieInfo.svp, 3),
        rating: new NumValue(goalieInfo.svpRate)
      }, {
        id: 'wins',
        label: this.$t('statNames.wins'),
        value: new NumValue(goalieInfo.wins, 0),
        rating: new NumValue(goalieInfo.winsRate)
      }, {
        id: 'winPercentage',
        label: this.$t('statNames.winPercentage'),
        value: new NumValue(goalieInfo.winPercentage),
        rating: new NumValue(goalieInfo.winPercentageRate)
      }, {
        id: 'shutout',
        label: this.$t('statNames.shutouts'),
        value: new NumValue(goalieInfo.shutout, 0),
        rating: new NumValue(goalieInfo.shutoutRate)
      }];
    },

    saveStats() {
      let goalieInfo = this.getGoalieInfo();
      if (goalieInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.savePercentage'),
        value: new NumValue(goalieInfo.svp, 3)
      }, {
        name: this.$t('statNames.saves'),
        value: new NumValue(goalieInfo.saves, 0)
      }, {
        name: this.$t('statNames.savesPerGame'),
        value: new NumValue(goalieInfo.savesPerGame)
      }, {
        name: this.$t('statNames.shotsAgainstPerGoal'),
        value: new NumValue(goalieInfo.shotsAgainstPerGoal)
      }];
    },

    goalStats() {
      let goalieInfo = this.getGoalieInfo();
      if (goalieInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.goalsAgainstAverage'),
        value: new NumValue(goalieInfo.gaa)
      }, {
        name: this.$t('statNames.goalsAgainst'),
        value: new NumValue(goalieInfo.goalsAgainst, 0)
      }, {
        name: this.$t('statNames.evenStrengthGoalsAgainst'),
        value: new NumValue(goalieInfo.evenStrengthGoalsAgainst, 0)
      }, {
        name: this.$t('statNames.evenStrengthGoalsAgainstPercentage'),
        value: new NumValue(goalieInfo.evenStrengthGoalsAgainstPercentage, 1)
      }, {
        name: this.$t('statNames.ppGoalsAllowed'),
        value: new NumValue(goalieInfo.ppGoalsAgainst, 0)
      }, {
        name: this.$t('statNames.shGoalsAllowed'),
        value: new NumValue(goalieInfo.shGoalsAgainst, 0)
      }];
    },

    homeStats() {
      let goalieInfo = this.getGoalieInfo();
      if (goalieInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.goalsAgainstAverage'),
        value: new NumValue(goalieInfo.homeGaa)
      }, {
        name: this.$t('statNames.savePercentage'),
        value: new NumValue(goalieInfo.homeSvp, 3)
      }, {
        name: this.$t('statNames.winPercentage'),
        value: new NumValue(goalieInfo.homeWinPercentage)
      }, {
        name: this.$t('statNames.wins'),
        value: new NumValue(goalieInfo.homeWins, 0)
      }];
    },

    awayStats() {
      let goalieInfo = this.getGoalieInfo();
      if (goalieInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.goalsAgainstAverage'),
        value: new NumValue(goalieInfo.awayGaa)
      }, {
        name: this.$t('statNames.savePercentage'),
        value: new NumValue(goalieInfo.awaySvp, 3)
      }, {
        name: this.$t('statNames.winPercentage'),
        value: new NumValue(goalieInfo.awayWinPercentage)
      }, {
        name: this.$t('statNames.wins'),
        value: new NumValue(goalieInfo.awayWins, 0)
      }];
    },

    chartData() {
      let goalieStats = this.getGoalieAllStats();
      if (goalieStats.length === 0) {
        return {};
      }
      if (this.selectedChart === CHART_GAA) {
        return {
          barChart: true,
          chartData: {
            dataSet: CompUtils.allStatsToChartData(goalieStats, [{from: 'gaa', to: 'y'}]),
            preciseYDomain: true,
            tooltipFormat: (t) => f3(t)
          }
        };
      }
      if (this.selectedChart === CHART_SP) {
        return {
          barChart: true,
          chartData: {
            dataSet: CompUtils.allStatsToChartData(goalieStats, [{from: 'svp', to: 'y'}]),
            preciseYDomain: true,
            tooltipFormat: (t) => f3(t)
          }
        };
      }
      if (this.selectedChart === CHART_WINS) {
        let data = CompUtils.allStatsToChartData(goalieStats, [
          {from: 'wins', to: 'wins'},
          {from: 'losses', to: 'losses'}
        ]);
        data.names = ['wins', 'losses'];
        return {
          stackedBarChart: true,
          chartData: {
            dataSet: data,
            legend: [
              {key: 'wins', name: this.$t('statNames.wins')},
              {key: 'losses', name: this.$t('statNames.losses')}
            ]
          }
        };
      }
      if (this.selectedChart === CHART_SHUTOUTS) {
        return {
          barChart: true,
          chartData: {
            dataSet: CompUtils.allStatsToChartData(goalieStats, [{from: 'shutout', to: 'y'}])
          }
        };
      }
      if (this.selectedChart === CHART_TOI) {
        return {
          barChart: true,
          chartData: {
            yCaption: this.$t('charts.toiCaptionY'),
            dataSet: CompUtils.allStatsToChartData(goalieStats, [{from: 'toi', to: 'y', convert: (t) => t / 60}]),
            tooltipFormat: (t) => CompUtils.toiToStr(t * 60)
          }
        };
      }
      return {};
    }
  },
  methods: {
    requestGoalieInfo() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getGoalieSeasonInfo', {
          playerId: this.$route.params.id,
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    },

    getGoalieInfo() {
      let season = this.$store.state.season.selectedSeason;
      let goalieInfo = this.$store.getters.getGoalieSeasonInfo(season, parseInt(this.$route.params.id));
      if (goalieInfo === null) {
        this.requestGoalieInfo();
      }
      return goalieInfo;
    },

    getGoalieAllStats() {
      let stats = this.$store.getters.getGoalieAllStats(parseInt(this.$route.params.id));
      if (stats === null) {
        this.$store.dispatch('getGoalieAllStats', {playerId: this.$route.params.id});
        return [];
      }
      return stats.seasons;
    }
  }
};

</script>

<style lang="less">
  .goalie-info__selectors {
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
    margin: 1rem 0;
    .goalie-info__selector {
      width: 70%;
    }
  }
</style>
