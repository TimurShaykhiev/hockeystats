<template>
  <div class="goalie-info container-col">
    <player-personal-info v-bind="playerInfo" v-if="playerInfo.id"/>
    <div class="goalie-info__season-picker container-row">
      <season-picker type="goalie"/>
    </div>
    <div class="container-row">
      <player-main-stat v-for="el in ratings" :key="el.id" v-bind="el"/>
    </div>
    <goalies-stats-table type="player"/>
    <stats-block :caption="$t('goalieInfo.saveStatistics')" :items="saveStats"/>
    <stats-block :caption="$t('goalieInfo.goalStatistics')" :items="goalStats"/>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import PlayerMainStat from 'Components/PlayerMainStat';
import PlayerPersonalInfo from 'Components/PlayerPersonalInfo';
import SeasonPicker from 'Components/SeasonPicker';
import StatsBlock from 'Components/StatsBlock';
import GoaliesStatsTable from 'Components/GoaliesStatsTable';

export default {
  name: 'goalie-info',
  components: {PlayerMainStat, SeasonPicker, StatsBlock, PlayerPersonalInfo, GoaliesStatsTable},
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
    return {};
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
        precision: 2,
        rating: goalieInfo.gaaRate
      }, {
        id: 'svp',
        label: this.$t('statNames.savePercentage'),
        value: goalieInfo.svp,
        precision: 3,
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
        precision: 2,
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
        precision: 3
      }, {
        name: this.$t('statNames.saves'),
        value: goalieInfo.saves
      }, {
        name: this.$t('statNames.savesPerGame'),
        value: goalieInfo.savesPerGame,
        precision: 2
      }, {
        name: this.$t('statNames.shotsAgainstPerGoal'),
        value: goalieInfo.shotsAgainstPerGoal,
        precision: 2
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
        precision: 2
      }, {
        name: this.$t('statNames.goalsAgainst'),
        value: goalieInfo.goalsAgainst
      }, {
        name: this.$t('statNames.evenStrengthGoalsAgainst'),
        value: goalieInfo.evenStrengthGoalsAgainst
      }, {
        name: this.$t('statNames.evenStrengthGoalsAgainstPercentage'),
        value: goalieInfo.evenStrengthGoalsAgainstPercentage,
        precision: 1,
        percentage: true
      }, {
        name: this.$t('statNames.ppGoalsAllowed'),
        value: goalieInfo.ppGoalsAgainst
      }, {
        name: this.$t('statNames.shGoalsAllowed'),
        value: goalieInfo.shGoalsAgainst
      }];
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
