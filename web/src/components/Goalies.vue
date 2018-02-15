<template>
  <div class="">
    <div class="goalies__season-picker container-row">
      <season-picker type="all"/>
    </div>
    <select class="chart-picker__select" v-model="selectedChart">
      <option v-for="el in chartList" :value="el.value" :disabled="el.disabled">{{el.name}}</option>
    </select>
    <bar-chart v-if="chartData.barChart" v-bind="chartData.chartData"/>
    <stacked-bar-chart v-else-if="chartData.stackedBarChart" v-bind="chartData.chartData"/>
    <goalies-stats-table type="all"/>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import {statsToChartData, toiToStr} from 'Components/utils';
import {format} from 'd3-format';

let f3 = format('.3f');

const CHART_GAA = 1;
const CHART_SP = 2;
const CHART_WINS = 3;
const CHART_SHUTOUTS = 4;
const CHART_TOI = 5;

const CHART_PLAYER_LIMIT = 50;

export default {
  name: 'goalies',
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
    this.requestGoalieStats();
  },
  computed: {
    chartData() {
      let selSeason = this.$store.state.season.selectedSeason;
      let stats = this.$store.getters.getGoalieStats(selSeason);
      if (stats === null) {
        this.requestGoalieStats();
        return {};
      }
      let goalieStats = stats.goalies;
      if (this.selectedChart === CHART_GAA) {
        return {
          barChart: true,
          chartData: {
            rotateXLabels: true,
            sorting: 'asc',
            limit: CHART_PLAYER_LIMIT,
            dataSet: statsToChartData(goalieStats, [{from: 'gaa', to: 'y'}]),
            preciseYDomain: true,
            tooltipFormat: (t) => f3(t)
          }
        };
      }
      if (this.selectedChart === CHART_SP) {
        return {
          barChart: true,
          chartData: {
            rotateXLabels: true,
            sorting: 'desc',
            limit: CHART_PLAYER_LIMIT,
            dataSet: statsToChartData(goalieStats, [{from: 'svp', to: 'y'}]),
            preciseYDomain: true,
            tooltipFormat: (t) => f3(t)
          }
        };
      }
      if (this.selectedChart === CHART_WINS) {
        let data = statsToChartData(goalieStats, [
          {from: 'wins', to: 'wins'},
          {from: 'losses', to: 'losses'}
        ]);
        data.names = ['wins', 'losses'];
        return {
          stackedBarChart: true,
          chartData: {
            rotateXLabels: true,
            sorting: 'desc',
            limit: CHART_PLAYER_LIMIT,
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
            rotateXLabels: true,
            sorting: 'desc',
            limit: CHART_PLAYER_LIMIT,
            dataSet: statsToChartData(goalieStats, [{from: 'shutout', to: 'y'}])
          }
        };
      }
      if (this.selectedChart === CHART_TOI) {
        return {
          barChart: true,
          chartData: {
            rotateXLabels: true,
            sorting: 'desc',
            limit: CHART_PLAYER_LIMIT,
            yCaption: this.$t('charts.toiCaptionY'),
            dataSet: statsToChartData(goalieStats, [{from: 'toi', to: 'y', convert: (t) => t / 60}]),
            tooltipFormat: (t) => toiToStr(t * 60)
          }
        };
      }
      return {};
    }
  },
  methods: {
    requestGoalieStats() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getGoalieStats', {
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    }
  }
};

</script>

<style lang="less">
  .goalies__season-picker {
    justify-content: flex-end;
    padding: 0 2rem;
    margin: 1rem 0;
  }
</style>
