<template>
  <div class="seasons">
    <h1 class="seasons__title">{{$t('title')}}</h1>
    <div class="seasons__season-picker-container container-row">
      <checkbox-switch v-model="showAllSeasons" textClasses="seasons__all-seasons-checkbox-text">
        {{$t('allSeasonsCheckbox')}}
      </checkbox-switch>
      <season-picker type="all"/>
    </div>
    <div v-if="showAllSeasons">
      <seasons-stats-table type="regular" class="seasons__season-table"/>
      <seasons-stats-table type="playoff" class="seasons__season-table"/>
    </div>
    <div v-else>
      <h2 class="seasons__season-caption">{{seasonCaption}}</h2>
      <stats-block :caption="$t('seasonInfo.seasonStatistics')" :items="seasonStatistics"/>
      <stats-block :caption="$t('seasonInfo.gameAverage')" :items="gameAverage"/>
      <stats-block :caption="$t('seasonInfo.winPercentage')" :items="winPercentage"/>
      <select class="chart-picker__select" v-model="selectedChart">
        <option v-for="el in chartList" :value="el.value" :disabled="el.disabled">{{el.name}}</option>
      </select>
      <pie-chart v-if="chartData.pieChart" v-bind="chartData.chartData"/>

      <h2 class="seasons__top-results-caption">{{$t('captions.teamsBest')}}</h2>
      <div class="seasons__top-results-container container-row">
        <season-top-result v-for="el in teamsBest" :key="el.id"  v-bind="el"/>
      </div>
      <h2 class="seasons__top-results-caption">{{$t('captions.teamsWorst')}}</h2>
      <div class="seasons__top-results-container container-row">
        <season-top-result v-for="el in teamsWorst" :key="el.id"  v-bind="el"/>
      </div>
      <h2 class="seasons__top-results-caption">{{$t('captions.skatersBest')}}</h2>
      <div class="seasons__top-results-container container-row">
        <season-top-result v-for="el in skatersBest" :key="el.id"  v-bind="el"/>
      </div>
      <h2 class="seasons__top-results-caption">{{$t('captions.skatersWorst')}}</h2>
      <div class="seasons__top-results-container container-row">
        <season-top-result v-for="el in skatersWorst" :key="el.id"  v-bind="el"/>
      </div>
      <h2 class="seasons__top-results-caption">{{$t('captions.forwardsBest')}}</h2>
      <div class="seasons__top-results-container container-row">
        <season-top-result v-for="el in forwardsBest" :key="el.id"  v-bind="el"/>
      </div>
      <h2 class="seasons__top-results-caption">{{$t('captions.forwardsWorst')}}</h2>
      <div class="seasons__top-results-container container-row">
        <season-top-result v-for="el in forwardsWorst" :key="el.id"  v-bind="el"/>
      </div>
      <h2 class="seasons__top-results-caption">{{$t('captions.defencemenBest')}}</h2>
      <div class="seasons__top-results-container container-row">
        <season-top-result v-for="el in defencemenBest" :key="el.id"  v-bind="el"/>
      </div>
      <h2 class="seasons__top-results-caption">{{$t('captions.defencemenWorst')}}</h2>
      <div class="seasons__top-results-container container-row">
        <season-top-result v-for="el in defencemenWorst" :key="el.id"  v-bind="el"/>
      </div>
      <h2 class="seasons__top-results-caption">{{$t('captions.goaliesBest')}}</h2>
      <div class="seasons__top-results-container container-row">
        <season-top-result v-for="el in goaliesBest" :key="el.id"  v-bind="el"/>
      </div>
      <h2 class="seasons__top-results-caption">{{$t('captions.goaliesWorst')}}</h2>
      <div class="seasons__top-results-container container-row">
        <season-top-result v-for="el in goaliesWorst" :key="el.id"  v-bind="el"/>
      </div>
    </div>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import CheckboxSwitch from 'Components/CheckboxSwitch';
import SeasonTopResult from 'Components/SeasonTopResult';
import CompUtils from 'Components/utils';
import {NumValue, TimeValue} from 'Components/statValue';

const CHART_PENALTIES = 1;

export default {
  name: 'seasons',
  components: {CheckboxSwitch, SeasonTopResult},
  i18n: {
    messages: {
      en: {
        title: 'Seasons',
        allSeasonsCheckbox: 'All seasons',
        seasonInfo: {
          seasonStatistics: 'SEASON STATISTICS',
          gameAverage: 'GAME AVERAGE STATISTICS',
          winPercentage: 'WIN PERCENTAGE'
        },
        captions: {
          teamsBest: 'Team best results',
          teamsWorst: 'Team worst results',
          skatersBest: 'Skater best results',
          skatersWorst: 'Skater worst results',
          forwardsBest: 'Forward best results',
          forwardsWorst: 'Forward worst results',
          defencemenBest: 'Defenceman best results',
          defencemenWorst: 'Defenceman worst results',
          goaliesBest: 'Goaltender best results',
          goaliesWorst: 'Goaltender worst results'
        }
      },
      ru: {
        title: 'Сезоны',
        allSeasonsCheckbox: 'Все сезоны',
        seasonInfo: {
          seasonStatistics: 'СТАТИСТИКА СЕЗОНА',
          gameAverage: 'СРЕДНИЕ ПОКАЗАТЕЛИ ЗА ИГРУ',
          winPercentage: 'ПРОЦЕНТ ПОБЕД'
        },
        captions: {
          teamsBest: 'Лучшие результаты команд',
          teamsWorst: 'Худшие результаты команд',
          skatersBest: 'Лучшие результаты игроков',
          skatersWorst: 'Худшие результаты игроков',
          forwardsBest: 'Лучшие результаты нападающих',
          forwardsWorst: 'Худшие результаты нападающих',
          defencemenBest: 'Лучшие результаты защитников',
          defencemenWorst: 'Худшие результаты защитников',
          goaliesBest: 'Лучшие результаты вратарей',
          goaliesWorst: 'Худшие результаты вратарей'
        }
      }
    }
  },
  data() {
    return {
      showAllSeasons: false,
      selectedChart: CHART_PENALTIES,
      chartList: [
        {name: this.$t('charts.penalties'), value: CHART_PENALTIES, disabled: false}
      ]
    };
  },
  created() {
    this.requestAllTeams();
    this.requestSeasonInfo();
  },
  computed: {
    seasonCaption() {
      let selSeason = this.$store.state.season.selectedSeason;
      if (selSeason.id === undefined) {
        return '';
      }
      return CompUtils.seasonToStr(selSeason);
    },

    seasonStatistics() {
      let seasonInfo = this.getSeasonInfo();
      if (seasonInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.games'),
        value: new NumValue(seasonInfo.stats.games, 0)
      }, {
        name: this.$t('statNames.ppPercentage'),
        value: new NumValue(seasonInfo.stats.ppPercentage)
      }];
    },

    gameAverage() {
      let seasonInfo = this.getSeasonInfo();
      if (seasonInfo === null) {
        return [];
      }
      return [{
        name: this.$t('statNames.goalsForPerGame'),
        value: new NumValue(seasonInfo.stats.goalsPerGame)
      }, {
        name: this.$t('statNames.shotsPerGame'),
        value: new NumValue(seasonInfo.stats.shotsPerGame)
      }, {
        name: this.$t('statNames.blocksPerGame'),
        value: new NumValue(seasonInfo.stats.blocksPerGame)
      }, {
        name: this.$t('statNames.hitsPerGame'),
        value: new NumValue(seasonInfo.stats.hitsPerGame)
      }, {
        name: this.$t('statNames.pimPerGame'),
        value: new NumValue(seasonInfo.stats.pimPerGame)
      }];
    },

    winPercentage() {
      let seasonInfo = this.getSeasonInfo();
      if (seasonInfo === null) {
        return [];
      }
      let result = [{
          name: this.$t('statNames.regularWinPercentage'),
          value: new NumValue(seasonInfo.stats.regularWinPercentage)
        }, {
          name: this.$t('statNames.overtimeWinPercentage'),
          value: new NumValue(seasonInfo.stats.overtimeWinPercentage)
        }];
      if (seasonInfo.season.regular) {
        result.push({
          name: this.$t('statNames.shootoutWinPercentage'),
          value: new NumValue(seasonInfo.stats.shootoutWinPercentage)
        });
      }
      return result;
    },

    teamsBest() {
      let allTeams = this.getAllTeams();
      let seasonInfo = this.getSeasonInfo();
      if (seasonInfo === null || allTeams === null) {
        return [];
      }
      allTeams = allTeams.teams;
      let tops = seasonInfo.tops;
      let result = [
        this.createTeamTopResult(tops, allTeams, 'goalsFor', true, 'goalsFor', 0),
        this.createTeamTopResult(tops, allTeams, 'goalsAgainstMin', true, 'goalsAgainst', 0),
        this.createTeamTopResult(tops, allTeams, 'ppp', true, 'ppPercentage'),
        this.createTeamTopResult(tops, allTeams, 'pkp', true, 'pkPercentage')
      ];
      if (seasonInfo.season.regular) {
        result.unshift(this.createTeamTopResult(tops, allTeams, 'teamPoints', true, 'points', 0));
      }
      return result;
    },

    teamsWorst() {
      let allTeams = this.getAllTeams();
      let seasonInfo = this.getSeasonInfo();
      if (seasonInfo === null || allTeams === null) {
        return [];
      }
      allTeams = allTeams.teams;
      let tops = seasonInfo.tops;
      let result = [
        this.createTeamTopResult(tops, allTeams, 'goalsForMin', false, 'goalsFor', 0),
        this.createTeamTopResult(tops, allTeams, 'goalsAgainst', false, 'goalsAgainst', 0),
        this.createTeamTopResult(tops, allTeams, 'pppMin', false, 'ppPercentage'),
        this.createTeamTopResult(tops, allTeams, 'pkpMin', false, 'pkPercentage')
      ];
      if (seasonInfo.season.regular) {
        result.unshift(this.createTeamTopResult(tops, allTeams, 'teamPointsMin', false, 'points', 0));
      }
      return result;
    },

    skatersBest() {
      let allTeams = this.getAllTeams();
      let seasonInfo = this.getSeasonInfo();
      if (seasonInfo === null || allTeams === null) {
        return [];
      }
      allTeams = allTeams.teams;
      let tops = seasonInfo.tops;
      let players = seasonInfo.players;
      return [
        this.createPlayerTopResult(tops, players, allTeams, 'goals', true, 'goals', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'assists', true, 'assists', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'points', true, 'points', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'ppGoals', true, 'ppGoals', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'ppPoints', true, 'ppPoints', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'plusMinus', true, 'plusMinus', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'turnover', true, 'turnover', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'fow', true, 'faceOffWinsPercentage'),
        this.createPlayerTopResult(tops, players, allTeams, 'shootingPrc', true, 'shootingPercentage'),
        this.createPlayerTopResult(tops, players, allTeams, 'pimMin', true, 'penaltyMinutes', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'toiPerGame', true, 'toiPerGame', -1),
        this.createPlayerTopResult(tops, players, allTeams, 'ppToiPerGame', true, 'ppToiPerGame', -1),
        this.createPlayerTopResult(tops, players, allTeams, 'shToiPerGame', true, 'shToiPerGame', -1),
        this.createPlayerTopResult(tops, players, allTeams, 'hitsPerGame', true, 'hitsPerGame'),
        this.createPlayerTopResult(tops, players, allTeams, 'blocksPerGame', true, 'blocksPerGame'),
        this.createPlayerTopResult(tops, players, allTeams, 'taPerGame', true, 'taPerGame')
      ];
    },

    skatersWorst() {
      let allTeams = this.getAllTeams();
      let seasonInfo = this.getSeasonInfo();
      if (seasonInfo === null || allTeams === null) {
        return [];
      }
      allTeams = allTeams.teams;
      let tops = seasonInfo.tops;
      let players = seasonInfo.players;
      return [
        this.createPlayerTopResult(tops, players, allTeams, 'plusMinusMin', false, 'plusMinus', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'turnoverMin', false, 'turnover', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'pim', false, 'penaltyMinutes', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'gaPerGame', false, 'gaPerGame')
      ];
    },

    forwardsBest() {
      let allTeams = this.getAllTeams();
      let seasonInfo = this.getSeasonInfo();
      if (seasonInfo === null || allTeams === null) {
        return [];
      }
      allTeams = allTeams.teams;
      let tops = seasonInfo.tops;
      let players = seasonInfo.players;
      return [
        this.createPlayerTopResult(tops, players, allTeams, 'fwdGoals', true, 'goals', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdAssists', true, 'assists', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdPoints', true, 'points', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdPpGoals', true, 'ppGoals', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdPpPoints', true, 'ppPoints', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdPlusMinus', true, 'plusMinus', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdTurnover', true, 'turnover', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdShootingPrc', true, 'shootingPercentage'),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdPimMin', true, 'penaltyMinutes', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdToiPerGame', true, 'toiPerGame', -1),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdPpToiPerGame', true, 'ppToiPerGame', -1),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdShToiPerGame', true, 'shToiPerGame', -1),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdHitsPerGame', true, 'hitsPerGame'),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdBlocksPerGame', true, 'blocksPerGame'),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdTaPerGame', true, 'taPerGame')
      ];
    },

    forwardsWorst() {
      let allTeams = this.getAllTeams();
      let seasonInfo = this.getSeasonInfo();
      if (seasonInfo === null || allTeams === null) {
        return [];
      }
      allTeams = allTeams.teams;
      let tops = seasonInfo.tops;
      let players = seasonInfo.players;
      return [
        this.createPlayerTopResult(tops, players, allTeams, 'fwdPlusMinusMin', false, 'plusMinus', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdTurnoverMin', false, 'turnover', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdPim', false, 'penaltyMinutes', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'fwdGaPerGame', false, 'gaPerGame')
      ];
    },

    defencemenBest() {
      let allTeams = this.getAllTeams();
      let seasonInfo = this.getSeasonInfo();
      if (seasonInfo === null || allTeams === null) {
        return [];
      }
      allTeams = allTeams.teams;
      let tops = seasonInfo.tops;
      let players = seasonInfo.players;
      return [
        this.createPlayerTopResult(tops, players, allTeams, 'defGoals', true, 'goals', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'defAssists', true, 'assists', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'defPoints', true, 'points', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'defPpGoals', true, 'ppGoals', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'defPpPoints', true, 'ppPoints', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'defPlusMinus', true, 'plusMinus', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'defTurnover', true, 'turnover', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'defShootingPrc', true, 'shootingPercentage'),
        this.createPlayerTopResult(tops, players, allTeams, 'defPimMin', true, 'penaltyMinutes', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'defToiPerGame', true, 'toiPerGame', -1),
        this.createPlayerTopResult(tops, players, allTeams, 'defPpToiPerGame', true, 'ppToiPerGame', -1),
        this.createPlayerTopResult(tops, players, allTeams, 'defShToiPerGame', true, 'shToiPerGame', -1),
        this.createPlayerTopResult(tops, players, allTeams, 'defHitsPerGame', true, 'hitsPerGame'),
        this.createPlayerTopResult(tops, players, allTeams, 'defBlocksPerGame', true, 'blocksPerGame'),
        this.createPlayerTopResult(tops, players, allTeams, 'defTaPerGame', true, 'taPerGame')
      ];
    },

    defencemenWorst() {
      let allTeams = this.getAllTeams();
      let seasonInfo = this.getSeasonInfo();
      if (seasonInfo === null || allTeams === null) {
        return [];
      }
      allTeams = allTeams.teams;
      let tops = seasonInfo.tops;
      let players = seasonInfo.players;
      return [
        this.createPlayerTopResult(tops, players, allTeams, 'defPlusMinusMin', false, 'plusMinus', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'defTurnoverMin', false, 'turnover', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'defPim', false, 'penaltyMinutes', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'defGaPerGame', false, 'gaPerGame')
      ];
    },

    goaliesBest() {
      let allTeams = this.getAllTeams();
      let seasonInfo = this.getSeasonInfo();
      if (seasonInfo === null || allTeams === null) {
        return [];
      }
      allTeams = allTeams.teams;
      let tops = seasonInfo.tops;
      let players = seasonInfo.players;
      return [
        this.createPlayerTopResult(tops, players, allTeams, 'glGames', true, 'games', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'glWins', true, 'wins', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'glShutouts', true, 'shutouts', 0),
        this.createPlayerTopResult(tops, players, allTeams, 'gaaMin', true, 'goalsAgainstAverage', 3),
        this.createPlayerTopResult(tops, players, allTeams, 'sp', true, 'savePercentage', 3),
        this.createPlayerTopResult(tops, players, allTeams, 'winPrc', true, 'winPercentage')
      ];
    },

    goaliesWorst() {
      let allTeams = this.getAllTeams();
      let seasonInfo = this.getSeasonInfo();
      if (seasonInfo === null || allTeams === null) {
        return [];
      }
      allTeams = allTeams.teams;
      let tops = seasonInfo.tops;
      let players = seasonInfo.players;
      return [
        this.createPlayerTopResult(tops, players, allTeams, 'gaa', false, 'goalsAgainstAverage', 3),
        this.createPlayerTopResult(tops, players, allTeams, 'spMin', false, 'savePercentage', 3),
        this.createPlayerTopResult(tops, players, allTeams, 'winPrcMin', false, 'winPercentage')
      ];
    },

    chartData() {
      if (this.selectedChart === CHART_PENALTIES) {
        let chartData = this.getChartData('seasonPenalties', 'getSeasonPenalties');
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
      }
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

    requestSeasonInfo() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getSeasonInfo', {
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    },

    getSeasonInfo() {
      let season = this.$store.state.season.selectedSeason;
      let seasonInfo = this.$store.getters.getSeasonInfo(season);
      if (seasonInfo === null) {
        this.requestSeasonInfo();
      }
      return seasonInfo;
    },

    getAllTeams() {
      let season = this.$store.state.season.selectedSeason;
      let allTeams = this.$store.getters.getAllTeams(season);
      if (allTeams === null) {
        this.requestAllTeams();
      }
      return allTeams;
    },

    createTeamTopResult(tops, allTeams, type, best, textResource, precision=2) {
      return {
        id: type,
        type: 'team',
        label: this.$t(`statNames.${textResource}`),
        value: new NumValue(tops[type].value, precision),
        names: tops[type].ids.map((id) => ({id: id, name: allTeams[id].name, routeName: 'team'})),
        best: best
      };
    },

    createPlayerTopResult(tops, players, allTeams, type, best, textResource, precision=2) {
      return {
        id: type,
        type: 'player',
        label: this.$t(`statNames.${textResource}`),
        value: precision > -1 ? new NumValue(tops[type].value, precision) : new TimeValue(tops[type].value),
        names: tops[type].ids.map((id) => ({
          id: id,
          name: players[id].name,
          team: allTeams[players[id].tid].name,
          pos: players[id].pos,
          routeName: players[id].pos === 'G' ? 'goalie' : 'skater'
        })),
        best: best
      };
    },

    getChartData(chartName, action) {
      let season = this.$store.state.season.selectedSeason;
      let chartData = this.$store.getters.getSeasonChartData(chartName, season);
      if (chartData === null) {
        if (season.id !== undefined) {
          this.$store.dispatch(action, {
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

  .seasons__title {
    text-align: center;
    margin: 1rem 0;
  }
  .seasons__all-seasons-checkbox-text {
    font-family: @header-font;
    font-size: 1.3rem;
  }
  .seasons__season-picker-container {
    justify-content: space-between;
    padding: 0 2rem;
    margin: 1rem 0;
  }
  .seasons__season-table {
    margin: 2rem 0;
  }
  .seasons__season-caption {
    text-align: center;
    margin: 2rem 0;
  }
  .seasons__top-results-caption {
    text-align: center;
    margin: 4rem 0 2rem 0;
  }
  .seasons__top-results-container {
    justify-content: space-between;
  }
</style>
