<template>
  <div class="teams">
    <h1 class="teams__title">{{$t('title')}}</h1>
    <div class="teams__season-picker container-row">
      <season-picker type="all"/>
    </div>
    <select class="chart-picker__select" v-model="selectedChart">
      <option v-for="el in chartList" :value="el.value" :disabled="el.disabled">{{el.name}}</option>
    </select>
    <bar-chart v-if="chartData.barChart" v-bind="chartData.chartData"/>
    <stacked-bar-chart v-else-if="chartData.stackedBarChart" v-bind="chartData.chartData"/>
    <teams-stats-table type="all"/>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import {format} from 'd3-format';
import CompUtils from 'Components/utils';

let f2 = format('.2f');

const CHART_POINTS = 1;
const CHART_WINS = 2;
const CHART_LOSSES = 3;
const CHART_PPP = 4;
const CHART_PKP = 5;
const CHART_GOALS_FOR = 6;
const CHART_GOALS_AGAINST = 7;
const CHART_GOALS_DIFF = 8;

export default {
  name: 'teams',
  i18n: {
    messages: {
      en: {
        title: 'Teams'
      },
      ru: {
        title: 'Команды'
      }
    }
  },
  created() {
    this.requestAllTeams();
    this.requestTeamStats();
  },
  computed: {
    selectedChart() {
      let selSeason = this.$store.state.season.selectedSeason;
      return selSeason.regular ? CHART_POINTS : CHART_WINS;
    },

    chartList() {
      let selSeason = this.$store.state.season.selectedSeason;
      let chartList = [
        {name: this.$t('charts.wins'), value: CHART_WINS},
        {name: this.$t('charts.losses'), value: CHART_LOSSES},
        {name: this.$t('charts.ppPercentage'), value: CHART_PPP},
        {name: this.$t('charts.pkPercentage'), value: CHART_PKP},
        {name: this.$t('charts.goalsFor'), value: CHART_GOALS_FOR},
        {name: this.$t('charts.goalsAgainst'), value: CHART_GOALS_AGAINST},
        {name: this.$t('charts.goalsDiff'), value: CHART_GOALS_DIFF}
      ];
      if (selSeason.regular) {
        chartList.unshift({name: this.$t('charts.points'), value: CHART_POINTS});
      }
      return chartList;
    },

    chartData() {
      let selSeason = this.$store.state.season.selectedSeason;
      let stats = this.$store.getters.getTeamStats(selSeason);
      if (stats === null) {
        this.requestTeamStats();
        return {};
      }
      let allTeams = this.$store.getters.getAllTeams(selSeason);
      if (allTeams === null) {
        this.requestAllTeams();
        return {};
      }
      allTeams = allTeams.teams;
      let getTeamName = (t) => allTeams[t.id].name;
      let teamStats = stats.teams;
      if (this.selectedChart === CHART_POINTS) {
        return {
          barChart: true,
          chartData: {
            rotateXLabels: true,
            sorting: 'desc',
            dataSet: CompUtils.statsToChartData(teamStats, [{from: 'points', to: 'y'}], getTeamName)
          }
        };
      }
      if (this.selectedChart === CHART_WINS) {
        let data = CompUtils.statsToChartData(teamStats, [
          {from: 'winRegular', to: 'winRegular'},
          {from: 'winOvertime', to: 'winOvertime'},
          {from: 'winShootout', to: 'winShootout'}
        ], getTeamName);
        data.names = ['winRegular', 'winOvertime', 'winShootout'];
        return {
          stackedBarChart: true,
          chartData: {
            rotateXLabels: true,
            sorting: 'desc',
            dataSet: data,
            legend: [
              {key: 'winRegular', name: this.$t('statNames.winRegular')},
              {key: 'winOvertime', name: this.$t('statNames.winOvertime')},
              {key: 'winShootout', name: this.$t('statNames.winShootout')}
            ]
          }
        };
      }
      if (this.selectedChart === CHART_LOSSES) {
        let data = CompUtils.statsToChartData(teamStats, [
          {from: 'loseRegular', to: 'loseRegular'},
          {from: 'loseOvertime', to: 'loseOvertime'},
          {from: 'loseShootout', to: 'loseShootout'}
        ], getTeamName);
        data.names = ['loseRegular', 'loseOvertime', 'loseShootout'];
        return {
          stackedBarChart: true,
          chartData: {
            rotateXLabels: true,
            sorting: 'desc',
            dataSet: data,
            legend: [
              {key: 'loseRegular', name: this.$t('statNames.loseRegular')},
              {key: 'loseOvertime', name: this.$t('statNames.loseOvertime')},
              {key: 'loseShootout', name: this.$t('statNames.loseShootout')}
            ]
          }
        };
      }
      if (this.selectedChart === CHART_PPP) {
        return {
          barChart: true,
          chartData: {
            rotateXLabels: true,
            sorting: 'desc',
            dataSet: CompUtils.statsToChartData(teamStats, [{from: 'ppPercentage', to: 'y'}], getTeamName),
            tooltipFormat: (t) => f2(t)
          }
        };
      }
      if (this.selectedChart === CHART_PKP) {
        return {
          barChart: true,
          chartData: {
            preciseYDomain: true,
            rotateXLabels: true,
            sorting: 'desc',
            dataSet: CompUtils.statsToChartData(teamStats, [{from: 'pkPercentage', to: 'y'}], getTeamName),
            tooltipFormat: (t) => f2(t)
          }
        };
      }
      if (this.selectedChart === CHART_GOALS_FOR) {
        return {
          barChart: true,
          chartData: {
            preciseYDomain: true,
            rotateXLabels: true,
            sorting: 'desc',
            dataSet: CompUtils.statsToChartData(teamStats, [{from: 'goalsFor', to: 'y'}], getTeamName)
          }
        };
      }
      if (this.selectedChart === CHART_GOALS_AGAINST) {
        return {
          barChart: true,
          chartData: {
            preciseYDomain: true,
            rotateXLabels: true,
            sorting: 'desc',
            dataSet: CompUtils.statsToChartData(teamStats, [{from: 'goalsAgainst', to: 'y'}], getTeamName)
          }
        };
      }
      if (this.selectedChart === CHART_GOALS_DIFF) {
        return {
          barChart: true,
          chartData: {
            preciseYDomain: true,
            rotateXLabels: true,
            sorting: 'desc',
            dataSet: CompUtils.statsToChartData(teamStats, [{from: 'goalsDiff', to: 'y'}], getTeamName)
          }
        };
      }
      return {};
    }
  },
  methods: {
    requestAllTeams() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getAllTeams', {
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    },

    requestTeamStats() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getTeamStats', {
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    }
  }
};

</script>

<style lang="less">
  .teams__title {
    text-align: center;
    margin: 1rem 0;
  }
  .teams__season-picker {
    justify-content: flex-end;
    padding: 0 2rem;
    margin: 1rem 0;
  }
</style>
