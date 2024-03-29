<template>
  <div class="">
    <h1 class="skaters__title">{{$t('title')}}</h1>
    <div class="skaters__season-picker container-row">
      <season-picker type="all"/>
    </div>
    <select class="chart-picker__select" v-model="selectedChart">
      <option v-for="el in chartList" :value="el.value" :disabled="el.disabled">{{el.name}}</option>
    </select>
    <bar-chart v-if="chartData.barChart" v-bind="chartData.chartData"/>
    <stacked-bar-chart v-else-if="chartData.stackedBarChart" v-bind="chartData.chartData"/>
    <skaters-stats-table type="all"/>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import {format} from 'd3-format';
import CompUtils from 'Components/utils';

let f2 = format('.2f');

const CHART_POINTS = 1;
const CHART_GOALS_ASSISTS = 2;
const CHART_GOALS = 3;
const CHART_ASSISTS = 4;
const CHART_TOI = 5;
const CHART_PLUS_MINUS = 6;
const CHART_POINTS_PER_GAME = 7;
const CHART_PIM = 8;
const CHART_FACE_OFF = 9;
const CHART_PENALTY_DREW_BY = 10;

const CHART_PLAYER_LIMIT = 50;

export default {
  name: 'skaters',
  i18n: {
    messages: {
      en: {
        title: 'Skaters'
      },
      ru: {
        title: 'Игроки'
      }
    }
  },
  data() {
    return {
      selectedChart: CHART_POINTS,
      chartList: [
        {name: this.$t('charts.points'), value: CHART_POINTS},
        {name: this.$t('charts.goalsAssists'), value: CHART_GOALS_ASSISTS},
        {name: this.$t('charts.goals'), value: CHART_GOALS},
        {name: this.$t('charts.assists'), value: CHART_ASSISTS},
        {name: this.$t('charts.toi'), value: CHART_TOI},
        {name: this.$t('charts.plusMinus'), value: CHART_PLUS_MINUS},
        {name: this.$t('charts.pointsPerGame'), value: CHART_POINTS_PER_GAME},
        {name: this.$t('charts.penaltyMinutes'), value: CHART_PIM},
        {name: this.$t('charts.faceoffWin'), value: CHART_FACE_OFF},
        {name: this.$t('charts.penaltyDrewBy'), value: CHART_PENALTY_DREW_BY}
      ]
    };
  },
  created() {
    this.requestSkaterStats();
  },
  computed: {
    chartData() {
      let selSeason = this.$store.state.season.selectedSeason;
      if (this.selectedChart === CHART_PENALTY_DREW_BY) {
        let chartData = this.getChartData('skatersPenaltyDrewBy', 'getSkatersPenaltyDrewBy');
        if (chartData === null) {
          return {};
        }
        return {
          barChart: true,
          chartData: {
            rotateXLabels: true,
            sorting: 'desc',
            limit: CHART_PLAYER_LIMIT,
            dataSet: CompUtils.nameValueToChartData(chartData.data)
          }
        };
      } else {
        let stats = this.$store.getters.getSkaterStats(selSeason);
        if (stats === null) {
          this.requestSkaterStats();
          return {};
        }
        let skaterStats = stats.skaters;
        if (this.selectedChart === CHART_GOALS_ASSISTS) {
          let data = CompUtils.statsToChartData(skaterStats, [
            {from: 'goals', to: 'goals'},
            {from: 'assists', to: 'assists'}
          ]);
          data.names = ['goals', 'assists'];
          return {
            stackedBarChart: true,
            chartData: {
              rotateXLabels: true,
              sorting: 'desc',
              limit: CHART_PLAYER_LIMIT,
              dataSet: data,
              legend: [
                {key: 'goals', name: this.$t('statNames.goals')},
                {key: 'assists', name: this.$t('statNames.assists')}
              ]
            }
          };
        }
        if (this.selectedChart === CHART_POINTS) {
          let data = CompUtils.statsToChartData(skaterStats, [
            {from: 'evenPoints', to: 'evenPoints'},
            {from: 'ppPoints', to: 'ppPoints'},
            {from: 'shPoints', to: 'shPoints'}
          ]);
          data.names = ['evenPoints', 'ppPoints', 'shPoints'];
          return {
            stackedBarChart: true,
            chartData: {
              rotateXLabels: true,
              sorting: 'desc',
              limit: CHART_PLAYER_LIMIT,
              dataSet: data,
              legend: [
                {key: 'evenPoints', name: this.$t('statNames.evenPoints')},
                {key: 'ppPoints', name: this.$t('statNames.ppPoints')},
                {key: 'shPoints', name: this.$t('statNames.shPoints')}
              ]
            }
          };
        }
        if (this.selectedChart === CHART_GOALS) {
          let data = CompUtils.statsToChartData(skaterStats, [
            {from: 'evenGoals', to: 'evenGoals'},
            {from: 'ppGoals', to: 'ppGoals'},
            {from: 'shGoals', to: 'shGoals'}
          ]);
          data.names = ['evenGoals', 'ppGoals', 'shGoals'];
          return {
            stackedBarChart: true,
            chartData: {
              rotateXLabels: true,
              sorting: 'desc',
              limit: CHART_PLAYER_LIMIT,
              dataSet: data,
              legend: [
                {key: 'evenGoals', name: this.$t('statNames.evenGoals')},
                {key: 'ppGoals', name: this.$t('statNames.ppGoals')},
                {key: 'shGoals', name: this.$t('statNames.shGoals')}
              ]
            }
          };
        }
        if (this.selectedChart === CHART_ASSISTS) {
          let data = CompUtils.statsToChartData(skaterStats, [
            {from: 'evenAssists', to: 'evenAssists'},
            {from: 'ppAssists', to: 'ppAssists'},
            {from: 'shAssists', to: 'shAssists'}
          ]);
          data.names = ['evenAssists', 'ppAssists', 'shAssists'];
          return {
            stackedBarChart: true,
            chartData: {
              rotateXLabels: true,
              sorting: 'desc',
              limit: CHART_PLAYER_LIMIT,
              dataSet: data,
              legend: [
                {key: 'evenAssists', name: this.$t('statNames.evenAssists')},
                {key: 'ppAssists', name: this.$t('statNames.ppAssists')},
                {key: 'shAssists', name: this.$t('statNames.shAssists')}
              ]
            }
          };
        }
        if (this.selectedChart === CHART_TOI) {
          return {
            barChart: true,
            chartData: {
              rotateXLabels: true,
              sorting: 'desc',
              yCaption: this.$t('charts.toiCaptionY'),
              limit: CHART_PLAYER_LIMIT,
              dataSet: CompUtils.statsToChartData(skaterStats, [{from: 'toiPerGame', to: 'y', convert: (t) => t / 60}]),
              tooltipFormat: (t) => CompUtils.toiToStr(t * 60)
            }
          };
        }
        if (this.selectedChart === CHART_PLUS_MINUS) {
          return {
            barChart: true,
            chartData: {
              rotateXLabels: true,
              sorting: 'desc',
              limit: CHART_PLAYER_LIMIT,
              dataSet: CompUtils.statsToChartData(skaterStats, [{from: 'plusMinus', to: 'y'}])
            }
          };
        }
        if (this.selectedChart === CHART_POINTS_PER_GAME) {
          return {
            barChart: true,
            chartData: {
              rotateXLabels: true,
              sorting: 'desc',
              limit: CHART_PLAYER_LIMIT,
              preciseYDomain: true,
              dataSet: CompUtils.statsToChartData(skaterStats, [{from: 'pointsPerGame', to: 'y'}]),
              tooltipFormat: (t) => f2(t)
            }
          };
        }
        if (this.selectedChart === CHART_PIM) {
          return {
            barChart: true,
            chartData: {
              rotateXLabels: true,
              sorting: 'desc',
              limit: CHART_PLAYER_LIMIT,
              dataSet: CompUtils.statsToChartData(skaterStats, [{from: 'penaltyMinutes', to: 'y'}])
            }
          };
        }
        if (this.selectedChart === CHART_FACE_OFF) {
          this.$store.dispatch('getSkaterStatsLimits', {season: selSeason});
          const faceOffTakenLimit = this.$store.state.players.skaterStatsLimits.limits.faceOffTaken;
          return {
            barChart: true,
            chartData: {
              rotateXLabels: true,
              sorting: 'desc',
              limit: CHART_PLAYER_LIMIT,
              dataSet: CompUtils.statsToChartData(skaterStats, [{
                from: 'faceOffWinsPercentage',
                to: 'y',
                filterFn: (d) => d > faceOffTakenLimit,
                filterField: 'faceOffTaken'
              }]),
              preciseYDomain: true,
              tooltipFormat: (t) => f2(t)
            }
          };
        }
      }
      return {};
    }
  },
  methods: {
    requestSkaterStats() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getSkaterStats', {
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    },

    getChartData(chartName, action) {
      let season = this.$store.state.season.selectedSeason;
      let chartData = this.$store.getters.getPlayersSeasonChartData(chartName, season);
      if (chartData === null) {
        if (season.id !== undefined) {
          this.$store.dispatch(action, {
            playerId: this.$route.params.id,
            reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
          });
        }
        return null;
      }
      return chartData;
    }
  }
};

</script>

<style lang="less">
  .skaters__title {
    text-align: center;
    margin: 1rem 0;
  }
  .skaters__season-picker {
    justify-content: flex-end;
    padding: 0 2rem;
    margin: 1rem 0;
  }
</style>
