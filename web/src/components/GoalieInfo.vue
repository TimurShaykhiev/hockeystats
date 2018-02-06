<template>
  <div class="goalie-info container-col">
    <player-personal-info v-bind="playerInfo" v-if="playerInfo.id"/>
    <div class="goalie-info__season-picker container-row">
      <season-picker type="goalie"/>
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
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import {allStatsToChartData, toiToStr} from 'Components/utils';
import {format} from 'd3-format';

let f1 = format('.1f');
let f2 = format('.2f');
let f3 = format('.3f');

const CHART_GAA = 1;
const CHART_SP = 2;
const CHART_WINS = 3;
const CHART_SHUTOUTS = 4;
const CHART_TOI = 5;

export default {
  name: 'goalie-info',
  components: {},
  props: {
  },
  i18n: {
    messages: {
      en: {
        goalieInfo: {
          saveStatistics: 'SAVES',
          goalStatistics: 'GOALS'
        }
      },
      ru: {
        goalieInfo: {
          saveStatistics: 'СПАСЕНИЯ',
          goalStatistics: 'ГОЛЫ'
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
      let selSeason = this.$store.state.season.selectedSeason;
      let goalieInfo = this.$store.state.players.goalieSeasonInfo;
      if (this.needRequest(goalieInfo, selSeason)) {
        this.requestGoalieInfo();
        return [];
      }
      return [{
        id: 'gaa',
        label: this.$t('statNames.goalsAgainstAverage'),
        value: goalieInfo.gaa,
        precision: f2,
        rating: goalieInfo.gaaRate
      }, {
        id: 'svp',
        label: this.$t('statNames.savePercentage'),
        value: goalieInfo.svp,
        precision: f3,
        rating: goalieInfo.svpRate
      }, {
        id: 'wins',
        label: this.$t('statNames.wins'),
        value: goalieInfo.wins,
        rating: goalieInfo.winsRate
      }, {
        id: 'winPercentage',
        label: this.$t('statNames.winPercentage'),
        value: goalieInfo.winPercentage,
        precision: f2,
        rating: goalieInfo.winPercentageRate
      }, {
        id: 'shutout',
        label: this.$t('statNames.shutouts'),
        value: goalieInfo.shutout,
        rating: goalieInfo.shutoutRate
      }];
    },

    saveStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let goalieInfo = this.$store.state.players.goalieSeasonInfo;
      if (this.needRequest(goalieInfo, selSeason)) {
        this.requestGoalieInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.savePercentage'),
        value: goalieInfo.svp,
        precision: f3
      }, {
        name: this.$t('statNames.saves'),
        value: goalieInfo.saves
      }, {
        name: this.$t('statNames.savesPerGame'),
        value: goalieInfo.savesPerGame,
        precision: f2
      }, {
        name: this.$t('statNames.shotsAgainstPerGoal'),
        value: goalieInfo.shotsAgainstPerGoal,
        precision: f2
      }];
    },

    goalStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let goalieInfo = this.$store.state.players.goalieSeasonInfo;
      if (this.needRequest(goalieInfo, selSeason)) {
        this.requestGoalieInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.goalsAgainstAverage'),
        value: goalieInfo.gaa,
        precision: f2
      }, {
        name: this.$t('statNames.goalsAgainst'),
        value: goalieInfo.goalsAgainst
      }, {
        name: this.$t('statNames.evenStrengthGoalsAgainst'),
        value: goalieInfo.evenStrengthGoalsAgainst
      }, {
        name: this.$t('statNames.evenStrengthGoalsAgainstPercentage'),
        value: goalieInfo.evenStrengthGoalsAgainstPercentage,
        precision: f1,
        percentage: true
      }, {
        name: this.$t('statNames.ppGoalsAllowed'),
        value: goalieInfo.ppGoalsAgainst
      }, {
        name: this.$t('statNames.shGoalsAllowed'),
        value: goalieInfo.shGoalsAgainst
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
            dataSet: allStatsToChartData(goalieStats, [{from: 'gaa', to: 'y'}]),
            preciseYDomain: true,
            tooltipFormat: (t) => f3(t)
          }
        };
      }
      if (this.selectedChart === CHART_SP) {
        return {
          barChart: true,
          chartData: {
            dataSet: allStatsToChartData(goalieStats, [{from: 'svp', to: 'y'}]),
            preciseYDomain: true,
            tooltipFormat: (t) => f3(t)
          }
        };
      }
      if (this.selectedChart === CHART_WINS) {
        let data = allStatsToChartData(goalieStats, [
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
            dataSet: allStatsToChartData(goalieStats, [{from: 'shutout', to: 'y'}])
          }
        };
      }
      if (this.selectedChart === CHART_TOI) {
        return {
          barChart: true,
          chartData: {
            yCaption: this.$t('charts.toiCaptionY'),
            dataSet: allStatsToChartData(goalieStats, [{from: 'toi', to: 'y', convert: (t) => t / 60}]),
            tooltipFormat: (t) => toiToStr(t * 60)
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

    needRequest(goalieInfo, selSeason) {
      return !goalieInfo.player || goalieInfo.player.id !== parseInt(this.$route.params.id) ||
             selSeason.id !== goalieInfo.season.id || selSeason.regular !== goalieInfo.season.regular;
    },

    getGoalieAllStats() {
      let stats = this.$store.state.players.goalieAllStats;
      if (!stats.player || stats.player.id !== parseInt(this.$route.params.id)) {
        this.$store.dispatch('getGoalieAllStats', {playerId: this.$route.params.id});
        return [];
      }
      return stats.seasons;
    }
  }
};

</script>

<style lang="less">
  .goalie-info__season-picker {
    justify-content: flex-end;
    padding: 0 2rem;
    margin: 1rem 0;
  }
</style>
