<template>
  <div class="goalies-compare container-col">
    <div class="container-row" v-if="playersInfo">
      <div class="goalies-compare__header container-row">
        <player-personal-info :playerInfo="playersInfo.left" :fullWidth="false" comparePosition="left"/>
      </div>
      <div class="goalies-compare__header container-row">
        <player-personal-info :playerInfo="playersInfo.right" :fullWidth="false" comparePosition="right"/>
      </div>
    </div>
    <div class="goalies-compare__main-stats container-row">
      <main-stat-compare v-for="el in mainStats" :key="el.id"  v-bind="el"/>
    </div>
    <div class="goalies-compare__compare-blocks container-row">
      <stats-compare-block v-if="saveStats" :caption="saveStats.caption" :items="saveStats.stats"/>
      <stats-compare-block v-if="goalStats" :caption="goalStats.caption" :items="goalStats.stats"/>
      <stats-compare-block v-if="homeStats" :caption="homeStats.caption" :items="homeStats.stats"/>
      <stats-compare-block v-if="awayStats" :caption="awayStats.caption" :items="awayStats.stats"/>
    </div>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import CompUtils from 'Components/utils';

export default {
  name: 'goalies-compare',
  i18n: {
    messages: {
      en: {
        goaliesCompare: {
          saveStatistics: 'SAVES',
          goalStatistics: 'GOALS',
          homeStatistics: 'HOME GAMES',
          awayStatistics: 'AWAY GAMES'
        }
      },
      ru: {
        goaliesCompare: {
          saveStatistics: 'СПАСЕНИЯ',
          goalStatistics: 'ГОЛЫ',
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
    this.requestGoaliesCompare();
  },
  computed: {
    playersInfo() {
      let data = this.getGoaliesCompare();
      if (data === null) {
        return undefined;
      }
      return {
        left: data.player1,
        right: data.player2
      };
    },

    mainStats() {
      let data = this.getGoaliesCompare();
      if (data === null) {
        return [];
      }
      return [
        CompUtils.createMainStatCompare(data, 'gaa', 'gaaRate', this.$t('statNames.goalsAgainstAverage'),
          CompUtils.getPlayerShortNames, 2, 'asc'),
        CompUtils.createMainStatCompare(data, 'svp', 'svpRate', this.$t('statNames.savePercentage'),
          CompUtils.getPlayerShortNames, 3),
        CompUtils.createMainStatCompare(data, 'wins', 'winsRate', this.$t('statNames.wins'),
          CompUtils.getPlayerShortNames, 0),
        CompUtils.createMainStatCompare(data, 'winPercentage', 'winPercentageRate', this.$t('statNames.winPercentage'),
          CompUtils.getPlayerShortNames),
        CompUtils.createMainStatCompare(data, 'shutout', 'shutoutRate', this.$t('statNames.shutouts'),
          CompUtils.getPlayerShortNames, 0)
      ];
    },

    saveStats() {
      let data = this.getGoaliesCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('goaliesCompare.saveStatistics'),
        CompUtils.getPlayerShortNames, [{
          name: this.$t('statNames.savePercentage'),
          attrName: 'svp',
          precision: 3
        }, {
          name: this.$t('statNames.saves'),
          attrName: 'saves',
          precision: 0
        }, {
          name: this.$t('statNames.savesPerGame'),
          attrName: 'savesPerGame'
        }, {
          name: this.$t('statNames.shotsAgainstPerGoal'),
          attrName: 'shotsAgainstPerGoal'
        }]
      );
    },

    goalStats() {
      let data = this.getGoaliesCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('goaliesCompare.goalStatistics'),
        CompUtils.getPlayerShortNames, [{
          name: this.$t('statNames.goalsAgainstAverage'),
          attrName: 'gaa',
          order: 'asc'
        }, {
          name: this.$t('statNames.goalsAgainst'),
          attrName: 'goalsAgainst',
          precision: 0,
          order: 'asc'
        }, {
          name: this.$t('statNames.evenStrengthGoalsAgainst'),
          attrName: 'evenStrengthGoalsAgainst',
          precision: 0,
          order: 'asc'
        }, {
          name: this.$t('statNames.evenStrengthGoalsAgainstPercentage'),
          attrName: 'evenStrengthGoalsAgainstPercentage',
          precision: 1,
          order: 'asc'
        }, {
          name: this.$t('statNames.ppGoalsAllowed'),
          attrName: 'ppGoalsAgainst',
          precision: 0,
          order: 'asc'
        }, {
          name: this.$t('statNames.shGoalsAllowed'),
          attrName: 'shGoalsAgainst',
          precision: 0,
          order: 'asc'
        }]
      );
    },

    homeStats() {
      let data = this.getGoaliesCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('goaliesCompare.homeStatistics'),
        CompUtils.getPlayerShortNames, [{
          name: this.$t('statNames.goalsAgainstAverage'),
          attrName: 'homeGaa',
          order: 'asc'
        }, {
          name: this.$t('statNames.savePercentage'),
          attrName: 'homeSvp',
          precision: 3
        }, {
          name: this.$t('statNames.winPercentage'),
          attrName: 'homeWinPercentage'
        }, {
          name: this.$t('statNames.wins'),
          attrName: 'homeWins',
          precision: 0
        }]
      );
    },

    awayStats() {
      let data = this.getGoaliesCompare();
      if (data === null) {
        return undefined;
      }
      return CompUtils.createStatCompare(data, this.$t('goaliesCompare.awayStatistics'),
        CompUtils.getPlayerShortNames, [{
          name: this.$t('statNames.goalsAgainstAverage'),
          attrName: 'awayGaa',
          order: 'asc'
        }, {
          name: this.$t('statNames.savePercentage'),
          attrName: 'awaySvp',
          precision: 3
        }, {
          name: this.$t('statNames.winPercentage'),
          attrName: 'awayWinPercentage'
        }, {
          name: this.$t('statNames.wins'),
          attrName: 'awayWins',
          precision: 0
        }]
      );
    }
  },
  methods: {
    requestGoaliesCompare() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getGoaliesComparison', {
          id1: this.pid1,
          id2: this.pid2,
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    },

    getGoaliesCompare() {
      let season = this.$store.state.season.selectedSeason;
      let data = this.$store.getters.getGoaliesComparison(season, this.pid1, this.pid2);
      if (data === null) {
        this.requestGoaliesCompare();
      }
      return data;
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .goalies-compare__header {
    align-items: center;
    padding: 0 1rem;
    flex: 1;
  }
  .goalies-compare__main-stats {
    margin: 2rem;
    flex-wrap: wrap;
  }
  .goalies-compare__compare-blocks {
    margin: 2rem;
    flex-wrap: wrap;
  }
</style>
