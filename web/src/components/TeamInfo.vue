<template>
  <div class="team-info container-col">
    <div class="team-info__caption container-row">
      <img :src="logoUrl" class="team-info__logo">
      <h1 class="team-info__name">{{teamName}}</h1>
    </div>
    <hr class="team-info__divider"/>
    <div class="team-info__selectors container-row">
      <item-selector class="team-info__selector" type="team"/>
      <season-picker class="team-info__season-picker" type="team"/>
    </div>
    <div class="container-row">
      <team-main-stat v-for="el in ratings" :key="el.id"  v-bind="el"/>
    </div>
    <tabs>
      <tab :name="$t('tabNames.charts')">
        <select class="chart-picker__select" v-model="selectedChart">
          <option v-for="el in chartList" :value="el.value" :disabled="el.disabled">{{el.name}}</option>
        </select>
        <bar-chart v-if="chartData.barChart" v-bind="chartData.chartData"/>
        <stacked-bar-chart v-else-if="chartData.stackedBarChart" v-bind="chartData.chartData"/>
        <radar-chart v-else-if="chartData.radarChart" v-bind="chartData.chartData"/>
        <line-chart v-else-if="chartData.lineChart" v-bind="chartData.chartData"/>
      </tab>
      <tab :name="$t('tabNames.table')">
        <teams-stats-table type="team"/>
        <skaters-stats-table type="team"/>
        <goalies-stats-table type="team"/>
      </tab>
    </tabs>
    <stats-block :caption="$t('teamInfo.goalStatistics')" :items="goalStats"/>
    <stats-block :caption="$t('teamInfo.shootingStatistics')" :items="shootingStats"/>
    <stats-block :caption="$t('teamInfo.advancedStatistics')" :items="advancedStats"/>
    <stats-block :caption="$t('teamInfo.ppStatistics')" :items="ppStats"/>
    <stats-block :caption="$t('teamInfo.pkStatistics')" :items="pkStats"/>
    <stats-block :caption="$t('teamInfo.goaltenderStatistics')" :items="goaltenderStats"/>
    <stats-block :caption="$t('teamInfo.homeStatistics')" :items="homeStats"/>
    <stats-block :caption="$t('teamInfo.awayStatistics')" :items="awayStats"/>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import TeamMainStat from 'Components/TeamMainStat';
import ItemSelector from 'Components/ItemSelector';
import {format} from 'd3-format';
import CompUtils from 'Components/utils';
import {NumValue} from 'Components/statValue';

let f2 = format('.2f');

// Team charts
const CHART_SKILLS = 1;
const CHART_HOME_AWAY = 2;
const CHART_POINTS = 3;
const CHART_WINS = 4;
const CHART_LOSSES = 5;
const CHART_PPP = 6;
const CHART_PKP = 7;
const CHART_POINTS_PROGRESS = 8;
// Team player charts
const CHART_GOALS_ASSISTS = 100;
const CHART_PLAYER_POINTS = 101;
const CHART_TOI = 102;
const CHART_PLUS_MINUS = 103;
const CHART_PIM = 104;
const CHART_GAMES = 105;
const CHART_POINTS_PER_GAME = 106;

export default {
  name: 'team-info',
  components: {TeamMainStat, ItemSelector},
  i18n: {
    messages: {
      en: {
        teamInfo: {
          goalStatistics: 'GOALS',
          shootingStatistics: 'SHOOTING',
          advancedStatistics: 'ADVANCED',
          ppStatistics: 'POWER PLAY',
          pkStatistics: 'PENALTY KILL',
          goaltenderStatistics: 'GOALTENDERS',
          homeStatistics: 'HOME STATISTICS',
          awayStatistics: 'AWAY STATISTICS',
          chartPickerTeam: '--- Team ---',
          chartPickerPlayers: '--- Players ---'
        }
      },
      ru: {
        teamInfo: {
          goalStatistics: 'ГОЛЫ',
          shootingStatistics: 'БРОСКИ',
          advancedStatistics: 'ДОПОЛНИТЕЛЬНАЯ СТАТИСТИКА',
          ppStatistics: 'РЕАЛИЗАЦИЯ БОЛЬШИНСТВА',
          pkStatistics: 'НЕЙТРАЛИЗАЦИЯ МЕНЬШИНСТВА',
          goaltenderStatistics: 'ВРАТАРИ',
          homeStatistics: 'СТАТИСТИКА В ДОМАШНИХ ИГРАХ',
          awayStatistics: 'СТАТИСТИКА В ГОСТЕВЫХ ИГРАХ',
          chartPickerTeam: '--- Команда ---',
          chartPickerPlayers: '--- Игроки ---'
        }
      }
    }
  },
  data() {
    return {
      selectedChart: CHART_POINTS,
      chartList: [
        {name: this.$t('teamInfo.chartPickerTeam'), value: 0, disabled: true},
        {name: this.$t('charts.points'), value: CHART_POINTS, disabled: false},
        {name: this.$t('charts.wins'), value: CHART_WINS, disabled: false},
        {name: this.$t('charts.losses'), value: CHART_LOSSES, disabled: false},
        {name: this.$t('charts.ppPercentage'), value: CHART_PPP, disabled: false},
        {name: this.$t('charts.pkPercentage'), value: CHART_PKP, disabled: false},
        {name: this.$t('charts.teamSkills'), value: CHART_SKILLS, disabled: false},
        {name: this.$t('charts.homeAway'), value: CHART_HOME_AWAY, disabled: false},
        {name: this.$t('charts.pointsProgress'), value: CHART_POINTS_PROGRESS, disabled: false},
        {name: this.$t('teamInfo.chartPickerPlayers'), value: 0, disabled: true},
        {name: this.$t('charts.goalsAssists'), value: CHART_GOALS_ASSISTS, disabled: false},
        {name: this.$t('charts.points'), value: CHART_PLAYER_POINTS, disabled: false},
        {name: this.$t('charts.toi'), value: CHART_TOI, disabled: false},
        {name: this.$t('charts.plusMinus'), value: CHART_PLUS_MINUS, disabled: false},
        {name: this.$t('charts.penaltyMinutes'), value: CHART_PIM, disabled: false},
        {name: this.$t('charts.games'), value: CHART_GAMES, disabled: false},
        {name: this.$t('charts.pointsPerGame'), value: CHART_POINTS_PER_GAME, disabled: false}
      ]
    };
  },
  created() {
    this.requestTeamInfo();
  },
  computed: {
    logoUrl() {
      return `images/team${this.$route.params.id}.svg`;
    },

    teamName() {
      let teamInfo = this.getTeamInfo();
      if (teamInfo === null) {
        return '';
      }
      return teamInfo.team.name;
    },

    ratings() {
      let teamInfo = this.getTeamInfo();
      if (teamInfo === null) {
        return [];
      }
      return [{
        id: 'goalsForPerGame',
        label: this.$t('statNames.goalsForPerGame'),
        value: new NumValue(teamInfo.goalsForPerGame),
        rating: new NumValue(teamInfo.goalsForPerGameRate),
        average: new NumValue(teamInfo.goalsForPerGameAvg)
      }, {
        id: 'goalsAgainstPerGame',
        label: this.$t('statNames.goalsAgainstPerGame'),
        value: new NumValue(teamInfo.goalsAgainstPerGame),
        rating: new NumValue(teamInfo.goalsAgainstPerGameRate),
        average: new NumValue(teamInfo.goalsAgainstPerGameAvg),
        sortOrder: 'asc'
      }, {
        id: 'ppPercentage',
        label: this.$t('statNames.ppPercentage'),
        value: new NumValue(teamInfo.ppPercentage),
        rating: new NumValue(teamInfo.ppPercentageRate),
        average: new NumValue(teamInfo.ppPercentageAvg)
      }, {
        id: 'pkPercentage',
        label: this.$t('statNames.pkPercentage'),
        value: new NumValue(teamInfo.pkPercentage),
        rating: new NumValue(teamInfo.pkPercentageRate),
        average: new NumValue(teamInfo.pkPercentageAvg)
      }, {
        id: 'shootingPercentage',
        label: this.$t('statNames.shootingPercentage'),
        value: new NumValue(teamInfo.shootingPercentage),
        rating: new NumValue(teamInfo.shootingPercentageRate),
        average: new NumValue(teamInfo.shootingPercentageAvg)
      }];
    },

    goalStats() {
      let teamInfo = this.getTeamInfo();
      if (teamInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.goalsFor'),
        value: new NumValue(teamInfo.goalsFor, 0)
      }, {
        name: this.$t('statNames.goalsForPerGame'),
        value: new NumValue(teamInfo.goalsForPerGame)
      }, {
        name: this.$t('statNames.goalsAgainst'),
        value: new NumValue(teamInfo.goalsAgainst, 0)
      }, {
        name: this.$t('statNames.goalsAgainstPerGame'),
        value: new NumValue(teamInfo.goalsAgainstPerGame)
      }];
    },

    shootingStats() {
      let teamInfo = this.getTeamInfo();
      if (teamInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.shotsPerGame'),
        value: new NumValue(teamInfo.shotsPerGame, 1)
      }, {
        name: this.$t('statNames.shotsAgainstPerGame'),
        value: new NumValue(teamInfo.shotsAgainstPerGame, 1)
      }, {
        name: this.$t('statNames.shootingPercentage'),
        value: new NumValue(teamInfo.shootingPercentage)
      }, {
        name: this.$t('statNames.oppShootingPercentage'),
        value: new NumValue(teamInfo.oppShootingPercentage)
      }];
    },

    advancedStats() {
      let teamInfo = this.getTeamInfo();
      if (teamInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.scoringEfficiencyRatio'),
        value: new NumValue(teamInfo.scoringEfficiencyRatio)
      }, {
        name: this.$t('statNames.shotEfficiencyRatio'),
        value: new NumValue(teamInfo.shotEfficiencyRatio)
      }, {
        name: this.$t('statNames.penaltyEfficiencyRatio'),
        value: new NumValue(teamInfo.penaltyEfficiencyRatio)
      }, {
        name: this.$t('statNames.pointsPerGame'),
        value: new NumValue(teamInfo.pointsPerGame)
      }, {
        name: this.$t('statNames.faceOffWinsPercentage'),
        value: new NumValue(teamInfo.faceOffWinsPercentage)
      }, {
        name: this.$t('statNames.shootoutWinPercentage'),
        value: new NumValue(teamInfo.shootoutWinPercentage)
      }];
    },

    ppStats() {
      let teamInfo = this.getTeamInfo();
      if (teamInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.ppPercentage'),
        value: new NumValue(teamInfo.ppPercentage)
      }, {
        name: this.$t('statNames.ppGoals'),
        value: new NumValue(teamInfo.ppGoals, 0)
      }, {
        name: this.$t('statNames.ppGoalsPerGame'),
        value: new NumValue(teamInfo.ppGoalsPerGame)
      }, {
        name: this.$t('statNames.ppPerGame'),
        value: new NumValue(teamInfo.ppPerGame)
      }];
    },

    pkStats() {
      let teamInfo = this.getTeamInfo();
      if (teamInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.pkPercentage'),
        value: new NumValue(teamInfo.pkPercentage)
      }, {
        name: this.$t('statNames.shGoalsAgainst'),
        value: new NumValue(teamInfo.shGoalsAgainst, 0)
      }, {
        name: this.$t('statNames.shGoalsAgainstPerGame'),
        value: new NumValue(teamInfo.shGoalsAgainstPerGame)
      }, {
        name: this.$t('statNames.shPerGame'),
        value: new NumValue(teamInfo.shPerGame)
      }];
    },

    goaltenderStats() {
      let teamInfo = this.getTeamInfo();
      if (teamInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.savePercentage'),
        value: new NumValue(teamInfo.savePercentage, 3)
      }, {
        name: this.$t('statNames.oppSavePercentage'),
        value: new NumValue(teamInfo.oppSavePercentage, 3)
      }, {
        name: this.$t('statNames.shutouts'),
        value: new NumValue(teamInfo.shutouts, 0)
      }, {
        name: this.$t('statNames.oppShutouts'),
        value: new NumValue(teamInfo.oppShutouts, 0)
      }];
    },

    homeStats() {
      let teamInfo = this.getTeamInfo();
      if (teamInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.goalsFor'),
        value: new NumValue(teamInfo.homeGoals, 0)
      }, {
        name: this.$t('statNames.goalsAgainst'),
        value: new NumValue(teamInfo.homeGoalsAgainst, 0)
      }, {
        name: this.$t('statNames.shots'),
        value: new NumValue(teamInfo.homeShots, 0)
      }, {
        name: this.$t('statNames.shotsAgainst'),
        value: new NumValue(teamInfo.homeShotsAgainst, 0)
      }, {
        name: this.$t('statNames.ppPercentage'),
        value: new NumValue(teamInfo.homePPPercentage)
      }, {
        name: this.$t('statNames.pkPercentage'),
        value: new NumValue(teamInfo.homePKPercentage)
      }, {
        name: this.$t('statNames.homeWinPercentage'),
        value: new NumValue(teamInfo.homeWinPercentage)
      }];
    },

    awayStats() {
      let teamInfo = this.getTeamInfo();
      if (teamInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.goalsFor'),
        value: new NumValue(teamInfo.awayGoals, 0)
      }, {
        name: this.$t('statNames.goalsAgainst'),
        value: new NumValue(teamInfo.awayGoalsAgainst, 0)
      }, {
        name: this.$t('statNames.shots'),
        value: new NumValue(teamInfo.awayShots, 0)
      }, {
        name: this.$t('statNames.shotsAgainst'),
        value: new NumValue(teamInfo.awayShotsAgainst, 0)
      }, {
        name: this.$t('statNames.ppPercentage'),
        value: new NumValue(teamInfo.awayPPPercentage)
      }, {
        name: this.$t('statNames.pkPercentage'),
        value: new NumValue(teamInfo.awayPKPercentage)
      }, {
        name: this.$t('statNames.awayWinPercentage'),
        value: new NumValue(teamInfo.awayWinPercentage)
      }];
    },

    chartData() {
      if (this.selectedChart === CHART_POINTS_PROGRESS) {
        let chartData = this.getChartData('teamPointsProgress', 'getTeamPointsProgress');
        if (chartData === null) {
          return {};
        }
        return {
          lineChart: true,
          chartData: {
            yCaption: this.$t('charts.points'),
            dataSet: {names: [chartData.tid], data: [chartData.data]}
          }
        };
      } else if (this.selectedChart < CHART_POINTS) {
        let teamInfo = this.getTeamInfo();
        if (teamInfo === null) {
          return {};
        }
        let selSeason = this.$store.state.season.selectedSeason;
        if (this.selectedChart === CHART_SKILLS) {
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
              dataSet: [CompUtils.seasonStatsToChartData(teamInfo, axises, teamInfo.team.id)]
            }
          };
        }
        if (this.selectedChart === CHART_HOME_AWAY) {
          let getRange = this.$store.getters.getTeamStatRange;
          let axises = [
            CompUtils.getAxis('haGoalsFor', this.$t('statNames.goalsFor'), getRange, selSeason.current),
            CompUtils.getAxis('haGoalsAgainst', this.$t('statNames.goalsAgainst'), getRange, selSeason.current),
            CompUtils.getAxis('haShots', this.$t('statNames.shots'), getRange, selSeason.current),
            CompUtils.getAxis('haShotsAgainst', this.$t('statNames.shotsAgainst'), getRange, selSeason.current),
            CompUtils.getAxis('haPpPercentage', this.$t('statNames.ppPercentage'), getRange, selSeason.current),
            CompUtils.getAxis('haPkPercentage', this.$t('statNames.pkPercentage'), getRange, selSeason.current)
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
                CompUtils.seasonStatsToChartData(teamInfo, axises, 'home', {
                  'haGoalsFor': 'homeGoals',
                  'haGoalsAgainst': 'homeGoalsAgainst',
                  'haShots': 'homeShots',
                  'haShotsAgainst': 'homeShotsAgainst',
                  'haPpPercentage': 'homePPPercentage',
                  'haPkPercentage': 'homePKPercentage'
                }),
                CompUtils.seasonStatsToChartData(teamInfo, axises, 'away', {
                  'haGoalsFor': 'awayGoals',
                  'haGoalsAgainst': 'awayGoalsAgainst',
                  'haShots': 'awayShots',
                  'haShotsAgainst': 'awayShotsAgainst',
                  'haPpPercentage': 'awayPPPercentage',
                  'haPkPercentage': 'awayPKPercentage'
                })
              ]
            }
          };
        }
      } else if (this.selectedChart < CHART_GOALS_ASSISTS) {
        let teamStats = this.getTeamAllStats();
        if (teamStats.length === 0) {
          return {};
        }
        if (this.selectedChart === CHART_POINTS) {
          return {
            barChart: true,
            chartData: {
              dataSet: CompUtils.allStatsToChartData(teamStats, [{from: 'points', to: 'y'}])
            }
          };
        }
        if (this.selectedChart === CHART_WINS) {
          let data = CompUtils.allStatsToChartData(teamStats, [
            {from: 'winRegular', to: 'winRegular'},
            {from: 'winOvertime', to: 'winOvertime'},
            {from: 'winShootout', to: 'winShootout'}
          ]);
          data.names = ['winRegular', 'winOvertime', 'winShootout'];
          return {
            stackedBarChart: true,
            chartData: {
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
          let data = CompUtils.allStatsToChartData(teamStats, [
            {from: 'loseRegular', to: 'loseRegular'},
            {from: 'loseOvertime', to: 'loseOvertime'},
            {from: 'loseShootout', to: 'loseShootout'}
          ]);
          data.names = ['loseRegular', 'loseOvertime', 'loseShootout'];
          return {
            stackedBarChart: true,
            chartData: {
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
              dataSet: CompUtils.allStatsToChartData(teamStats, [{from: 'ppPercentage', to: 'y'}]),
              tooltipFormat: (t) => f2(t)
            }
          };
        }
        if (this.selectedChart === CHART_PKP) {
          return {
            barChart: true,
            chartData: {
              dataSet: CompUtils.allStatsToChartData(teamStats, [{from: 'pkPercentage', to: 'y'}]),
              tooltipFormat: (t) => f2(t)
            }
          };
        }
      } else {
        let stats = this.getTeamPlayersStats();
        if (stats === null) {
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
              dataSet: data,
              legend: [
                {key: 'goals', name: this.$t('statNames.goals')},
                {key: 'assists', name: this.$t('statNames.assists')}
              ]
            }
          };
        }
        if (this.selectedChart === CHART_PLAYER_POINTS) {
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
              dataSet: data,
              legend: [
                {key: 'evenPoints', name: this.$t('statNames.evenPoints')},
                {key: 'ppPoints', name: this.$t('statNames.ppPoints')},
                {key: 'shPoints', name: this.$t('statNames.shPoints')}
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
              dataSet: CompUtils.statsToChartData(skaterStats, [{from: 'plusMinus', to: 'y'}])
            }
          };
        }
        if (this.selectedChart === CHART_PIM) {
          return {
            barChart: true,
            chartData: {
              rotateXLabels: true,
              sorting: 'desc',
              dataSet: CompUtils.statsToChartData(skaterStats, [{from: 'penaltyMinutes', to: 'y'}])
            }
          };
        }
        if (this.selectedChart === CHART_GAMES) {
          return {
            barChart: true,
            chartData: {
              rotateXLabels: true,
              sorting: 'desc',
              dataSet: CompUtils.statsToChartData(skaterStats, [{from: 'games', to: 'y'}])
            }
          };
        }
        if (this.selectedChart === CHART_POINTS_PER_GAME) {
          return {
            barChart: true,
            chartData: {
              rotateXLabels: true,
              sorting: 'desc',
              dataSet: CompUtils.statsToChartData(skaterStats, [{from: 'pointsPerGame', to: 'y'}]),
              tooltipFormat: (t) => f2(t)
            }
          };
        }
      }
      return {};
    }
  },
  methods: {
    requestTeamInfo() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getTeamSeasonInfo', {
          teamId: this.$route.params.id,
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    },

    getTeamInfo() {
      let season = this.$store.state.season.selectedSeason;
      let teamInfo = this.$store.getters.getTeamSeasonInfo(season, parseInt(this.$route.params.id));
      if (teamInfo === null) {
        this.requestTeamInfo();
      }
      return teamInfo;
    },

    getTeamAllStats() {
      let stats = this.$store.getters.getTeamAllStats(parseInt(this.$route.params.id));
      if (stats === null) {
        this.$store.dispatch('getTeamAllStats', {teamId: this.$route.params.id});
        return [];
      }
      return stats.seasons;
    },

    getTeamPlayersStats() {
      let season = this.$store.state.season.selectedSeason;
      let stats = this.$store.getters.getTeamPlayersStats(season, parseInt(this.$route.params.id));
      if (stats === null) {
        this.$store.dispatch('getTeamPlayersStats', {
          teamId: this.$route.params.id,
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
        return null;
      }
      return stats;
    },

    getChartData(chartName, action) {
      let season = this.$store.state.season.selectedSeason;
      let chartData = this.$store.getters.getTeamSeasonChartData(chartName, season, parseInt(this.$route.params.id));
      if (chartData === null) {
        if (season.id !== undefined) {
          this.$store.dispatch(action, {
            teamId: this.$route.params.id,
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
  @import '../../styles/vars.less';

  .team-info__caption {
    align-items: center;
    padding: 0 3rem;
  }
  .team-info__logo {
    width: 10rem;
    height: 10rem;
  }
  .team-info__name {
    font-size: 4rem;
    margin: 0 0 0 2.5rem;
  }
  .team-info__selectors {
    justify-content: space-between;
    align-items: center;
    padding: 0 2rem;
    margin: 1rem 0;
    .team-info__selector {
      width: 70%;
    }
  }
  .team-info__divider {
    background: @border-color;
    height: .25rem;
    width: 95%;
    margin: 1rem 2.5%;
    border: none;
  }
</style>
