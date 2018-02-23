<template>
  <div class="skater-info container-col">
    <player-personal-info v-bind="playerInfo" v-if="playerInfo.id"/>
    <div class="skater-info__season-picker container-row">
      <season-picker type="skater"/>
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
        <radar-chart v-else-if="chartData.radarChart" v-bind="chartData.chartData"/>
      </tab>
      <tab :name="$t('tabNames.table')">
        <skaters-stats-table type="player"/>
      </tab>
    </tabs>
    <stats-block :caption="$t('skaterInfo.pointStatistics')" :items="pointStats"/>
    <stats-block :caption="$t('skaterInfo.goalStatistics')" :items="goalStats"/>
    <stats-block :caption="$t('skaterInfo.assistStatistics')" :items="assistStats"/>
    <stats-block :caption="$t('skaterInfo.shootingStatistics')" :items="shootingStats"/>
    <stats-block :caption="$t('skaterInfo.takeawayStatistics')" :items="takeawayStats"/>
    <stats-block :caption="$t('skaterInfo.advancedStatistics')" :items="advancedStats"/>
    <stats-block :caption="$t('skaterInfo.homeStatistics')" :items="homeStats"/>
    <stats-block :caption="$t('skaterInfo.awayStatistics')" :items="awayStats"/>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import {allStatsToChartData, toiToStr, seasonStatsToChartData, getAxis} from 'Components/utils';
import {format} from 'd3-format';

let f1 = format('.1f');
let f2 = format('.2f');

const CHART_POINT = 1;
const CHART_GOALS_ASSISTS = 2;
const CHART_GOALS = 3;
const CHART_ASSISTS = 4;
const CHART_TOI = 5;
const CHART_SKILLS = 6;
const CHART_PLUS_MINUS = 7;
const CHART_POINTS_PER_GAME = 8;
const CHART_HOME_AWAY = 9;

export default {
  name: 'skater-info',
  components: {},
  i18n: {
    messages: {
      en: {
        skaterInfo: {
          pointStatistics: 'POINTS',
          goalStatistics: 'GOALS',
          assistStatistics: 'ASSISTS',
          shootingStatistics: 'SHOOTING',
          takeawayStatistics: 'TAKEAWAYS',
          advancedStatistics: 'ADVANCED',
          homeStatistics: 'HOME STATISTICS',
          awayStatistics: 'AWAY STATISTICS'
        }
      },
      ru: {
        skaterInfo: {
          pointStatistics: 'ОЧКИ',
          goalStatistics: 'ГОЛЫ',
          assistStatistics: 'ПАСЫ',
          shootingStatistics: 'БРОСКИ',
          takeawayStatistics: 'ОТБОРЫ',
          advancedStatistics: 'ДОПОЛНИТЕЛЬНАЯ СТАТИСТИКА',
          homeStatistics: 'СТАТИСТИКА В ДОМАШНИХ ИГРАХ',
          awayStatistics: 'СТАТИСТИКА В ГОСТЕВЫХ ИГРАХ'
        }
      }
    }
  },
  data() {
    return {
      selectedChart: CHART_POINT,
      chartList: [
        {name: this.$t('charts.points'), value: CHART_POINT},
        {name: this.$t('charts.goalsAssists'), value: CHART_GOALS_ASSISTS},
        {name: this.$t('charts.goals'), value: CHART_GOALS},
        {name: this.$t('charts.assists'), value: CHART_ASSISTS},
        {name: this.$t('charts.toi'), value: CHART_TOI},
        {name: this.$t('charts.skaterSkills'), value: CHART_SKILLS},
        {name: this.$t('charts.homeAway'), value: CHART_HOME_AWAY},
        {name: this.$t('charts.plusMinus'), value: CHART_PLUS_MINUS},
        {name: this.$t('charts.pointsPerGame'), value: CHART_POINTS_PER_GAME}
      ]
    };
  },
  created() {
    this.requestSkaterInfo();
  },
  computed: {
    playerInfo() {
      let skaterInfo = this.$store.state.players.skaterSeasonInfo;
      if (!skaterInfo.player) {
        return {};
      }
      return skaterInfo.player;
    },

    ratings() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        id: 'goals',
        label: this.$t('statNames.goals'),
        value: skaterInfo.goals,
        rating: skaterInfo.goalsRateTotal,
        teamRating: skaterInfo.goalsRateTeam
      }, {
        id: 'assists',
        label: this.$t('statNames.assists'),
        value: skaterInfo.assists,
        rating: skaterInfo.assistsRateTotal,
        teamRating: skaterInfo.assistsRateTeam
      }, {
        id: 'points',
        label: this.$t('statNames.points'),
        value: skaterInfo.points,
        rating: skaterInfo.pointsRateTotal,
        teamRating: skaterInfo.pointsRateTeam
      }, {
        id: 'plusMinus',
        label: this.$t('statNames.plusMinus'),
        value: skaterInfo.plusMinus,
        rating: skaterInfo.plusMinusRateTotal,
        teamRating: skaterInfo.plusMinusRateTeam
      }, {
        id: 'turnover',
        label: this.$t('statNames.turnover'),
        value: skaterInfo.turnover,
        rating: skaterInfo.turnoverRateTotal,
        teamRating: skaterInfo.turnoverRateTeam
      }];
    },

    pointStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.points'),
        value: skaterInfo.points
      }, {
        name: this.$t('statNames.pointsPerGame'),
        value: skaterInfo.pointsPerGame,
        precision: f2
      }, {
        name: this.$t('statNames.pointsPer60min'),
        value: skaterInfo.pointsPer60min,
        precision: f2
      }, {
        name: this.$t('statNames.goalPercentageOfPoints'),
        value: skaterInfo.goalPercentageOfPoints,
        precision: f1,
        percentage: true
      }, {
        name: this.$t('statNames.assistPercentageOfPoints'),
        value: skaterInfo.assistPercentageOfPoints,
        precision: f1,
        percentage: true
      }];
    },

    goalStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.goals'),
        value: skaterInfo.goals
      }, {
        name: this.$t('statNames.goalsPerGame'),
        value: skaterInfo.goalsPerGame,
        precision: f2
      }, {
        name: this.$t('statNames.goalsPer60min'),
        value: skaterInfo.goalsPer60min,
        precision: f2
      }, {
        name: this.$t('statNames.evenStrengthGoalsPercentage'),
        value: skaterInfo.evenStrengthGoalsPercentage,
        precision: f1,
        percentage: true
      }, {
        name: this.$t('statNames.ppGoalPercentage'),
        value: skaterInfo.ppGoalPercentage,
        precision: f1,
        percentage: true
      }];
    },

    assistStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.assists'),
        value: skaterInfo.assists
      }, {
        name: this.$t('statNames.assistsPerGame'),
        value: skaterInfo.assistsPerGame,
        precision: f2
      }, {
        name: this.$t('statNames.assistsPer60min'),
        value: skaterInfo.assistsPer60min,
        precision: f2
      }, {
        name: this.$t('statNames.evenAssistPercentage'),
        value: skaterInfo.evenAssistPercentage,
        precision: f1,
        percentage: true
      }, {
        name: this.$t('statNames.ppAssistPercentage'),
        value: skaterInfo.ppAssistPercentage,
        precision: f1,
        percentage: true
      }];
    },

    shootingStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.shootingPercentage'),
        value: skaterInfo.shootingPercentage,
        precision: f1,
        percentage: true
      }, {
        name: this.$t('statNames.shots'),
        value: skaterInfo.shots
      }, {
        name: this.$t('statNames.shotsPerGame'),
        value: skaterInfo.shotsPerGame,
        precision: f1
      }, {
        name: this.$t('statNames.shotsPer60min'),
        value: skaterInfo.shotsPer60min,
        precision: f1
      }, {
        name: this.$t('statNames.shotsPerGoal'),
        value: skaterInfo.shotsPerGoal,
        precision: f1
      }];
    },

    takeawayStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.takeaways'),
        value: skaterInfo.takeaways
      }, {
        name: this.$t('statNames.giveaways'),
        value: skaterInfo.giveaways
      }, {
        name: this.$t('statNames.turnover'),
        value: skaterInfo.turnover
      }, {
        name: this.$t('statNames.turnoverPer60min'),
        value: skaterInfo.turnoverPer60min,
        precision: f2
      }, {
        name: this.$t('statNames.turnoverRatio'),
        value: skaterInfo.turnoverRatio,
        precision: f2
      }];
    },

    advancedStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.plusMinus'),
        value: skaterInfo.plusMinus
      }, {
        name: this.$t('statNames.blocks'),
        value: skaterInfo.blocks
      }, {
        name: this.$t('statNames.blocksPer60min'),
        value: skaterInfo.blocksPer60min,
        precision: f1
      }, {
        name: this.$t('statNames.hits'),
        value: skaterInfo.hits
      }, {
        name: this.$t('statNames.hitsPer60min'),
        value: skaterInfo.hitsPer60min,
        precision: f1
      }, {
        name: this.$t('statNames.toiPerGame'),
        value: skaterInfo.toiPerGame,
        time: true
      }, {
        name: this.$t('statNames.faceOffWinsPercentage'),
        value: skaterInfo.faceOffWinsPercentage,
        precision: f1,
        percentage: true
      }, {
        name: this.$t('statNames.penaltyMinutes'),
        value: skaterInfo.penaltyMinutes
      }, {
        name: this.$t('statNames.PIMsPer60min'),
        value: skaterInfo.PIMsPer60min,
        precision: f2
      }];
    },

    homeStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.goalsFor'),
        value: skaterInfo.homeGoals
      }, {
        name: this.$t('statNames.assists'),
        value: skaterInfo.homeAssists
      }, {
        name: this.$t('statNames.plusMinus'),
        value: skaterInfo.homePlusMinus
      }, {
        name: this.$t('statNames.turnover'),
        value: skaterInfo.homeTurnover
      }, {
        name: this.$t('statNames.pointsPerGame'),
        value: skaterInfo.homePointsPerGame,
        precision: f2
      }, {
        name: this.$t('statNames.penaltyMinutes'),
        value: skaterInfo.homePim
      }];
    },

    awayStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.goalsFor'),
        value: skaterInfo.awayGoals
      }, {
        name: this.$t('statNames.assists'),
        value: skaterInfo.awayAssists
      }, {
        name: this.$t('statNames.plusMinus'),
        value: skaterInfo.awayPlusMinus
      }, {
        name: this.$t('statNames.turnover'),
        value: skaterInfo.awayTurnover
      }, {
        name: this.$t('statNames.pointsPerGame'),
        value: skaterInfo.awayPointsPerGame,
        precision: f2
      }, {
        name: this.$t('statNames.penaltyMinutes'),
        value: skaterInfo.awayPim
      }];
    },

    chartData() {
      if (this.selectedChart === CHART_SKILLS || this.selectedChart === CHART_HOME_AWAY) {
        let skaterInfo = this.getSkaterInfo();
        if (skaterInfo === null) {
          return {};
        }
        let selSeason = this.$store.state.season.selectedSeason;
        if (this.selectedChart === CHART_SKILLS) {
          let getRange = this.$store.getters.getSkaterStatRange;
          let axises = [
            getAxis('goals', this.$t('statNames.goals'), getRange, selSeason.current),
            getAxis('assists', this.$t('statNames.assists'), getRange, selSeason.current),
            getAxis('plusMinus', this.$t('statNames.plusMinus'), getRange, selSeason.current),
            getAxis('turnover', this.$t('statNames.turnover'), getRange, selSeason.current),
            getAxis('penaltyMinutes', this.$t('statNames.penaltyMinutes'), getRange, selSeason.current)
          ];
          return {
            radarChart: true,
            chartData: {
              homogeneous: false,
              axises: axises,
              dataSet: [seasonStatsToChartData(skaterInfo, axises, skaterInfo.player.id)]
            }
          };
        }
        if (this.selectedChart === CHART_HOME_AWAY) {
          let getRange = this.$store.getters.getSkaterStatRange;
          let axises = [
            getAxis('haGoals', this.$t('statNames.goals'), getRange, selSeason.current),
            getAxis('haAssists', this.$t('statNames.assists'), getRange, selSeason.current),
            getAxis('haPlusMinus', this.$t('statNames.plusMinus'), getRange, selSeason.current),
            getAxis('haTurnover', this.$t('statNames.turnover'), getRange, selSeason.current),
            getAxis('haPointsPerGame', this.$t('statNames.pointsPerGame'), getRange, selSeason.current),
            getAxis('haPenaltyMinutes', this.$t('statNames.penaltyMinutes'), getRange, selSeason.current)
          ];
          return {
            radarChart: true,
            chartData: {
              homogeneous: false,
              axises: axises,
              legend: [
                {key: 'home', name: this.$t('charts.homeGames')},
                {key: 'away', name: this.$t('charts.awayGames')}
              ],
              dataSet: [
                seasonStatsToChartData(skaterInfo, axises, 'home', {
                  'haGoals': 'homeGoals',
                  'haAssists': 'homeAssists',
                  'haPlusMinus': 'homePlusMinus',
                  'haTurnover': 'homeTurnover',
                  'haPointsPerGame': 'homePointsPerGame',
                  'haPenaltyMinutes': 'homePim'
                }),
                seasonStatsToChartData(skaterInfo, axises, 'away', {
                  'haGoals': 'awayGoals',
                  'haAssists': 'awayAssists',
                  'haPlusMinus': 'awayPlusMinus',
                  'haTurnover': 'awayTurnover',
                  'haPointsPerGame': 'awayPointsPerGame',
                  'haPenaltyMinutes': 'awayPim'
                })
              ]
            }
          };
        }
      } else {
        let skaterStats = this.getSkaterAllStats();
        if (skaterStats.length === 0) {
          return {};
        }
        if (this.selectedChart === CHART_GOALS_ASSISTS) {
          let data = allStatsToChartData(skaterStats, [
            {from: 'goals', to: 'goals'},
            {from: 'assists', to: 'assists'}
          ]);
          data.names = ['goals', 'assists'];
          return {
            stackedBarChart: true,
            chartData: {
              dataSet: data,
              legend: [
                {key: 'goals', name: this.$t('statNames.goals')},
                {key: 'assists', name: this.$t('statNames.assists')}
              ]
            }
          };
        }
        if (this.selectedChart === CHART_POINT) {
          let data = allStatsToChartData(skaterStats, [
            {from: 'evenPoints', to: 'evenPoints'},
            {from: 'ppPoints', to: 'ppPoints'},
            {from: 'shPoints', to: 'shPoints'}
          ]);
          data.names = ['evenPoints', 'ppPoints', 'shPoints'];
          return {
            stackedBarChart: true,
            chartData: {
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
          let data = allStatsToChartData(skaterStats, [
            {from: 'evenGoals', to: 'evenGoals'},
            {from: 'ppGoals', to: 'ppGoals'},
            {from: 'shGoals', to: 'shGoals'}
          ]);
          data.names = ['evenGoals', 'ppGoals', 'shGoals'];
          return {
            stackedBarChart: true,
            chartData: {
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
          let data = allStatsToChartData(skaterStats, [
            {from: 'evenAssists', to: 'evenAssists'},
            {from: 'ppAssists', to: 'ppAssists'},
            {from: 'shAssists', to: 'shAssists'}
          ]);
          data.names = ['evenAssists', 'ppAssists', 'shAssists'];
          return {
            stackedBarChart: true,
            chartData: {
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
              yCaption: this.$t('charts.toiCaptionY'),
              dataSet: allStatsToChartData(skaterStats, [{from: 'toiPerGame', to: 'y', convert: (t) => t / 60}]),
              tooltipFormat: (t) => toiToStr(t * 60)
            }
          };
        }
        if (this.selectedChart === CHART_PLUS_MINUS) {
          return {
            barChart: true,
            chartData: {
              dataSet: allStatsToChartData(skaterStats, [{from: 'plusMinus', to: 'y'}])
            }
          };
        }
        if (this.selectedChart === CHART_POINTS_PER_GAME) {
          return {
            barChart: true,
            chartData: {
              dataSet: allStatsToChartData(skaterStats, [{from: 'pointsPerGame', to: 'y'}]),
              tooltipFormat: (t) => f2(t)
            }
          };
        }
      }
      return {};
    }
  },
  methods: {
    requestSkaterInfo() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getSkaterSeasonInfo', {
          playerId: this.$route.params.id,
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    },

    getSkaterInfo() {
      let season = this.$store.state.season.selectedSeason;
      let skaterInfo = this.$store.getters.getSkaterSeasonInfo(season, parseInt(this.$route.params.id));
      if (skaterInfo === null) {
        this.requestSkaterInfo();
      }
      return skaterInfo;
    },

    getSkaterAllStats() {
      let stats = this.$store.getters.getSkaterAllStats(parseInt(this.$route.params.id));
      if (stats === null) {
        this.$store.dispatch('getSkaterAllStats', {playerId: this.$route.params.id});
        return [];
      }
      return stats.seasons;
    }
  }
};

</script>

<style lang="less">
  .skater-info__season-picker {
    justify-content: flex-end;
    padding: 0 2rem;
    margin: 1rem 0;
  }
</style>
