<template>
  <div class="skater-info container-col">
    <player-personal-info v-bind="playerInfo" v-if="playerInfo.id"/>
    <div class="skater-info__season-picker container-row">
      <season-picker type="skater"/>
    </div>
    <div class="container-row">
      <player-main-stat v-for="el in ratings" :key="el.id" v-bind="el"/>
    </div>
    <stats-block :caption="$t('skaterInfo.pointStatistics')" :items="pointStats"/>
    <stats-block :caption="$t('skaterInfo.goalStatistics')" :items="goalStats"/>
    <stats-block :caption="$t('skaterInfo.assistStatistics')" :items="assistStats"/>
    <stats-block :caption="$t('skaterInfo.shootingStatistics')" :items="shootingStats"/>
    <stats-block :caption="$t('skaterInfo.takeawayStatistics')" :items="takeawayStats"/>
    <stats-block :caption="$t('skaterInfo.advancedStatistics')" :items="advancedStats"/>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import PlayerMainStat from 'Components/PlayerMainStat';
import PlayerPersonalInfo from 'Components/PlayerPersonalInfo';
import SeasonPicker from 'Components/SeasonPicker';
import StatsBlock from 'Components/StatsBlock';

export default {
  name: 'skater-info',
  components: {PlayerMainStat, SeasonPicker, StatsBlock, PlayerPersonalInfo},
  props: {
  },
  i18n: {
    messages: {
      en: {
        skaterInfo: {
          pointStatistics: 'POINTS',
          goalStatistics: 'GOALS',
          assistStatistics: 'ASSISTS',
          shootingStatistics: 'SHOOTING',
          takeawayStatistics: 'TAKEAWAYS',
          advancedStatistics: 'ADVANCED'
        }
      },
      ru: {
        skaterInfo: {
          pointStatistics: 'ОЧКИ',
          goalStatistics: 'ГОЛЫ',
          assistStatistics: 'ПАСЫ',
          shootingStatistics: 'БРОСКИ',
          takeawayStatistics: 'ОТБОРЫ',
          advancedStatistics: 'ДОПОЛНИТЕЛЬНАЯ СТАТИСТИКА'
        }
      }
    }
  },
  data() {
    return {};
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
      let selSeason = this.$store.state.season.selectedSeason;
      let skaterInfo = this.$store.state.players.skaterSeasonInfo;
      if (this.needRequest(skaterInfo, selSeason)) {
        this.requestSkaterInfo();
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
      let selSeason = this.$store.state.season.selectedSeason;
      let skaterInfo = this.$store.state.players.skaterSeasonInfo;
      if (this.needRequest(skaterInfo, selSeason)) {
        this.requestSkaterInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.points'),
        value: skaterInfo.points
      }, {
        name: this.$t('statNames.pointsPerGame'),
        value: skaterInfo.pointsPerGame,
        precision: 2
      }, {
        name: this.$t('statNames.pointsPer60min'),
        value: skaterInfo.pointsPer60min,
        precision: 2
      }, {
        name: this.$t('statNames.goalPercentageOfPoints'),
        value: skaterInfo.goalPercentageOfPoints,
        precision: 1,
        percentage: true
      }, {
        name: this.$t('statNames.assistPercentageOfPoints'),
        value: skaterInfo.assistPercentageOfPoints,
        precision: 1,
        percentage: true
      }];
    },

    goalStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let skaterInfo = this.$store.state.players.skaterSeasonInfo;
      if (this.needRequest(skaterInfo, selSeason)) {
        this.requestSkaterInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.goals'),
        value: skaterInfo.goals
      }, {
        name: this.$t('statNames.goalsPerGame'),
        value: skaterInfo.goalsPerGame,
        precision: 2
      }, {
        name: this.$t('statNames.goalsPer60min'),
        value: skaterInfo.goalsPer60min,
        precision: 2
      }, {
        name: this.$t('statNames.evenStrengthGoalsPercentage'),
        value: skaterInfo.evenStrengthGoalsPercentage,
        precision: 1,
        percentage: true
      }, {
        name: this.$t('statNames.ppGoalPercentage'),
        value: skaterInfo.ppGoalPercentage,
        precision: 1,
        percentage: true
      }];
    },

    assistStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let skaterInfo = this.$store.state.players.skaterSeasonInfo;
      if (this.needRequest(skaterInfo, selSeason)) {
        this.requestSkaterInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.assists'),
        value: skaterInfo.assists
      }, {
        name: this.$t('statNames.assistsPerGame'),
        value: skaterInfo.assistsPerGame,
        precision: 2
      }, {
        name: this.$t('statNames.assistsPer60min'),
        value: skaterInfo.assistsPer60min,
        precision: 2
      }, {
        name: this.$t('statNames.evenAssistPercentage'),
        value: skaterInfo.evenAssistPercentage,
        precision: 1,
        percentage: true
      }, {
        name: this.$t('statNames.ppAssistPercentage'),
        value: skaterInfo.ppAssistPercentage,
        precision: 1,
        percentage: true
      }];
    },

    shootingStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let skaterInfo = this.$store.state.players.skaterSeasonInfo;
      if (this.needRequest(skaterInfo, selSeason)) {
        this.requestSkaterInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.shootingPercentage'),
        value: skaterInfo.shootingPercentage,
        precision: 1,
        percentage: true
      }, {
        name: this.$t('statNames.shots'),
        value: skaterInfo.shots
      }, {
        name: this.$t('statNames.shotsPerGame'),
        value: skaterInfo.shotsPerGame,
        precision: 1
      }, {
        name: this.$t('statNames.shotsPer60min'),
        value: skaterInfo.shotsPer60min,
        precision: 1
      }, {
        name: this.$t('statNames.shotsPerGoal'),
        value: skaterInfo.shotsPerGoal,
        precision: 1
      }];
    },

    takeawayStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let skaterInfo = this.$store.state.players.skaterSeasonInfo;
      if (this.needRequest(skaterInfo, selSeason)) {
        this.requestSkaterInfo();
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
        precision: 2
      }, {
        name: this.$t('statNames.turnoverRatio'),
        value: skaterInfo.turnoverRatio,
        precision: 2
      }];
    },

    advancedStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let skaterInfo = this.$store.state.players.skaterSeasonInfo;
      if (this.needRequest(skaterInfo, selSeason)) {
        this.requestSkaterInfo();
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
        precision: 1
      }, {
        name: this.$t('statNames.hits'),
        value: skaterInfo.hits
      }, {
        name: this.$t('statNames.hitsPer60min'),
        value: skaterInfo.hitsPer60min,
        precision: 1
      }, {
        name: this.$t('statNames.toiPerGame'),
        value: skaterInfo.toiPerGame,
        time: true
      }, {
        name: this.$t('statNames.faceOffWinsPercentage'),
        value: skaterInfo.faceOffWinsPercentage,
        precision: 1,
        percentage: true
      }, {
        name: this.$t('statNames.penaltyMinutes'),
        value: skaterInfo.penaltyMinutes
      }, {
        name: this.$t('statNames.PIMsPer60min'),
        value: skaterInfo.PIMsPer60min,
        precision: 2
      }];
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

    needRequest(skaterInfo, selSeason) {
      return !skaterInfo.player || skaterInfo.player.id !== parseInt(this.$route.params.id) ||
             selSeason.id !== skaterInfo.season.id || selSeason.regular !== skaterInfo.season.regular;
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
