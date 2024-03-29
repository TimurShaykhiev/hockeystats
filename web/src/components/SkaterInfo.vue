<template>
  <div class="skater-info container-col">
    <player-personal-info :playerInfo="playerInfo" v-if="playerInfo.id"/>
    <div class="skater-info__selectors container-row">
      <item-selector class="skater-info__selector" type="skater"/>
      <season-picker class="skater-info__season-picker" type="skater"/>
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
        <line-chart v-else-if="chartData.lineChart" v-bind="chartData.chartData"/>
        <pie-chart v-else-if="chartData.pieChart" v-bind="chartData.chartData"/>
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
import ItemSelector from 'Components/ItemSelector';
import CompUtils from 'Components/utils';
import {format} from 'd3-format';
import {NumValue, TimeValue} from 'Components/statValue';

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
const CHART_POINTS_PROGRESS = 10;
const CHART_PENALTIES = 11;

export default {
  name: 'skater-info',
  components: {ItemSelector},
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
        {name: this.$t('charts.pointsPerGame'), value: CHART_POINTS_PER_GAME},
        {name: this.$t('charts.pointsProgress'), value: CHART_POINTS_PROGRESS},
        {name: this.$t('charts.penalties'), value: CHART_PENALTIES}
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
        value: new NumValue(skaterInfo.goals, 0),
        rating: new NumValue(skaterInfo.goalsRateTotal),
        teamRating: new NumValue(skaterInfo.goalsRateTeam)
      }, {
        id: 'assists',
        label: this.$t('statNames.assists'),
        value: new NumValue(skaterInfo.assists, 0),
        rating: new NumValue(skaterInfo.assistsRateTotal),
        teamRating: new NumValue(skaterInfo.assistsRateTeam)
      }, {
        id: 'points',
        label: this.$t('statNames.points'),
        value: new NumValue(skaterInfo.points, 0),
        rating: new NumValue(skaterInfo.pointsRateTotal),
        teamRating: new NumValue(skaterInfo.pointsRateTeam)
      }, {
        id: 'plusMinus',
        label: this.$t('statNames.plusMinus'),
        value: new NumValue(skaterInfo.plusMinus, 0),
        rating: new NumValue(skaterInfo.plusMinusRateTotal),
        teamRating: new NumValue(skaterInfo.plusMinusRateTeam)
      }, {
        id: 'turnover',
        label: this.$t('statNames.turnover'),
        value: new NumValue(skaterInfo.turnover, 0),
        rating: new NumValue(skaterInfo.turnoverRateTotal),
        teamRating: new NumValue(skaterInfo.turnoverRateTeam)
      }];
    },

    pointStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.points'),
        value: new NumValue(skaterInfo.points, 0)
      }, {
        name: this.$t('statNames.pointsPerGame'),
        value: new NumValue(skaterInfo.pointsPerGame)
      }, {
        name: this.$t('statNames.pointsPer60min'),
        value: new NumValue(skaterInfo.pointsPer60min)
      }, {
        name: this.$t('statNames.goalPercentageOfPoints'),
        value: new NumValue(skaterInfo.goalPercentageOfPoints, 1)
      }, {
        name: this.$t('statNames.assistPercentageOfPoints'),
        value: new NumValue(skaterInfo.assistPercentageOfPoints, 1)
      }];
    },

    goalStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.goals'),
        value: new NumValue(skaterInfo.goals, 0)
      }, {
        name: this.$t('statNames.goalsPerGame'),
        value: new NumValue(skaterInfo.goalsPerGame)
      }, {
        name: this.$t('statNames.goalsPer60min'),
        value: new NumValue(skaterInfo.goalsPer60min)
      }, {
        name: this.$t('statNames.evenStrengthGoalsPercentage'),
        value: new NumValue(skaterInfo.evenStrengthGoalsPercentage, 1)
      }, {
        name: this.$t('statNames.ppGoalPercentage'),
        value: new NumValue(skaterInfo.ppGoalPercentage, 1)
      }];
    },

    assistStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.assists'),
        value: new NumValue(skaterInfo.assists, 0)
      }, {
        name: this.$t('statNames.assistsPerGame'),
        value: new NumValue(skaterInfo.assistsPerGame)
      }, {
        name: this.$t('statNames.assistsPer60min'),
        value: new NumValue(skaterInfo.assistsPer60min)
      }, {
        name: this.$t('statNames.evenAssistPercentage'),
        value: new NumValue(skaterInfo.evenAssistPercentage, 1)
      }, {
        name: this.$t('statNames.ppAssistPercentage'),
        value: new NumValue(skaterInfo.ppAssistPercentage, 1)
      }];
    },

    shootingStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.shootingPercentage'),
        value: new NumValue(skaterInfo.shootingPercentage, 1)
      }, {
        name: this.$t('statNames.shots'),
        value: new NumValue(skaterInfo.shots, 0)
      }, {
        name: this.$t('statNames.shotsPerGame'),
        value: new NumValue(skaterInfo.shotsPerGame, 1)
      }, {
        name: this.$t('statNames.shotsPer60min'),
        value: new NumValue(skaterInfo.shotsPer60min, 1)
      }, {
        name: this.$t('statNames.shotsPerGoal'),
        value: new NumValue(skaterInfo.shotsPerGoal, 1)
      }];
    },

    takeawayStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.takeaways'),
        value: new NumValue(skaterInfo.takeaways, 0)
      }, {
        name: this.$t('statNames.giveaways'),
        value: new NumValue(skaterInfo.giveaways, 0)
      }, {
        name: this.$t('statNames.turnover'),
        value: new NumValue(skaterInfo.turnover, 0)
      }, {
        name: this.$t('statNames.turnoverPer60min'),
        value: new NumValue(skaterInfo.turnoverPer60min)
      }, {
        name: this.$t('statNames.turnoverRatio'),
        value: new NumValue(skaterInfo.turnoverRatio)
      }];
    },

    advancedStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.plusMinus'),
        value: new NumValue(skaterInfo.plusMinus, 0)
      }, {
        name: this.$t('statNames.blocks'),
        value: new NumValue(skaterInfo.blocks, 0)
      }, {
        name: this.$t('statNames.blocksPer60min'),
        value: new NumValue(skaterInfo.blocksPer60min, 1)
      }, {
        name: this.$t('statNames.hits'),
        value: new NumValue(skaterInfo.hits, 0)
      }, {
        name: this.$t('statNames.hitsPer60min'),
        value: new NumValue(skaterInfo.hitsPer60min, 1)
      }, {
        name: this.$t('statNames.toiPerGame'),
        value: new TimeValue(skaterInfo.toiPerGame)
      }, {
        name: this.$t('statNames.faceOffWinsPercentage'),
        value: new NumValue(skaterInfo.faceOffWinsPercentage, 1)
      }, {
        name: this.$t('statNames.penaltyMinutes'),
        value: new NumValue(skaterInfo.penaltyMinutes, 0)
      }, {
        name: this.$t('statNames.PIMsPer60min'),
        value: new NumValue(skaterInfo.PIMsPer60min)
      }];
    },

    homeStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.goalsFor'),
        value: new NumValue(skaterInfo.homeGoals, 0)
      }, {
        name: this.$t('statNames.assists'),
        value: new NumValue(skaterInfo.homeAssists, 0)
      }, {
        name: this.$t('statNames.plusMinus'),
        value: new NumValue(skaterInfo.homePlusMinus, 0)
      }, {
        name: this.$t('statNames.turnover'),
        value: new NumValue(skaterInfo.homeTurnover, 0)
      }, {
        name: this.$t('statNames.pointsPerGame'),
        value: new NumValue(skaterInfo.homePointsPerGame)
      }, {
        name: this.$t('statNames.penaltyMinutes'),
        value: new NumValue(skaterInfo.homePim, 0)
      }];
    },

    awayStats() {
      let skaterInfo = this.getSkaterInfo();
      if (skaterInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.goalsFor'),
        value: new NumValue(skaterInfo.awayGoals, 0)
      }, {
        name: this.$t('statNames.assists'),
        value: new NumValue(skaterInfo.awayAssists, 0)
      }, {
        name: this.$t('statNames.plusMinus'),
        value: new NumValue(skaterInfo.awayPlusMinus, 0)
      }, {
        name: this.$t('statNames.turnover'),
        value: new NumValue(skaterInfo.awayTurnover, 0)
      }, {
        name: this.$t('statNames.pointsPerGame'),
        value: new NumValue(skaterInfo.awayPointsPerGame)
      }, {
        name: this.$t('statNames.penaltyMinutes'),
        value: new NumValue(skaterInfo.awayPim, 0)
      }];
    },

    chartData() {
      if (this.selectedChart === CHART_POINTS_PROGRESS) {
        let chartData = this.getChartData('skaterPointsProgress', 'getSkaterPointsProgress');
        if (chartData === null) {
          return {};
        }
        return {
          lineChart: true,
          chartData: {
            yCaption: this.$t('charts.points'),
            dataSet: {names: [chartData.pid], data: [chartData.data]}
          }
        };
      } else if (this.selectedChart === CHART_PENALTIES) {
        let chartData = this.getChartData('skaterPenalties', 'getSkaterPenalties');
        if (chartData === null) {
          return {};
        }
        let data = CompUtils.getPenaltiesPieChartData(chartData.data);
        return {
          pieChart: true,
          chartData: {
            dataSet: data.chartData,
            legend: data.legend
          }
        };
      } else if (this.selectedChart === CHART_SKILLS || this.selectedChart === CHART_HOME_AWAY) {
        let skaterInfo = this.getSkaterInfo();
        if (skaterInfo === null) {
          return {};
        }
        let selSeason = this.$store.state.season.selectedSeason;
        if (this.selectedChart === CHART_SKILLS) {
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
              dataSet: [CompUtils.seasonStatsToChartData(skaterInfo, axises, skaterInfo.player.id)]
            }
          };
        }
        if (this.selectedChart === CHART_HOME_AWAY) {
          let getRange = this.$store.getters.getSkaterStatRange;
          let axises = [
            CompUtils.getAxis('haGoals', this.$t('statNames.goals'), getRange, selSeason.current),
            CompUtils.getAxis('haAssists', this.$t('statNames.assists'), getRange, selSeason.current),
            CompUtils.getAxis('haPlusMinus', this.$t('statNames.plusMinus'), getRange, selSeason.current),
            CompUtils.getAxis('haTurnover', this.$t('statNames.turnover'), getRange, selSeason.current),
            CompUtils.getAxis('haPointsPerGame', this.$t('statNames.pointsPerGame'), getRange, selSeason.current),
            CompUtils.getAxis('haPenaltyMinutes', this.$t('statNames.penaltyMinutes'), getRange, selSeason.current)
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
                CompUtils.seasonStatsToChartData(skaterInfo, axises, 'home', {
                  'haGoals': 'homeGoals',
                  'haAssists': 'homeAssists',
                  'haPlusMinus': 'homePlusMinus',
                  'haTurnover': 'homeTurnover',
                  'haPointsPerGame': 'homePointsPerGame',
                  'haPenaltyMinutes': 'homePim'
                }),
                CompUtils.seasonStatsToChartData(skaterInfo, axises, 'away', {
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
          let data = CompUtils.allStatsToChartData(skaterStats, [
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
          let data = CompUtils.allStatsToChartData(skaterStats, [
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
          let data = CompUtils.allStatsToChartData(skaterStats, [
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
          let data = CompUtils.allStatsToChartData(skaterStats, [
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
              dataSet: CompUtils.allStatsToChartData(skaterStats, [{
                from: 'toiPerGame',
                to: 'y',
                convert: (t) => t / 60
              }]),
              tooltipFormat: (t) => CompUtils.toiToStr(t * 60)
            }
          };
        }
        if (this.selectedChart === CHART_PLUS_MINUS) {
          return {
            barChart: true,
            chartData: {
              dataSet: CompUtils.allStatsToChartData(skaterStats, [{from: 'plusMinus', to: 'y'}])
            }
          };
        }
        if (this.selectedChart === CHART_POINTS_PER_GAME) {
          return {
            barChart: true,
            chartData: {
              dataSet: CompUtils.allStatsToChartData(skaterStats, [{from: 'pointsPerGame', to: 'y'}]),
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
    },

    getChartData(chartName, action) {
      let season = this.$store.state.season.selectedSeason;
      let chartData = this.$store.getters.getPlayerSeasonChartData(chartName, season, parseInt(this.$route.params.id));
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
  .skater-info__selectors {
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
    margin: 1rem 0;
    .skater-info__selector {
      width: 70%;
    }
  }
</style>
