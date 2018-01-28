<template>
  <div class="team-info container-col">
    <div class="team-info__caption container-row">
      <img :src="logoUrl" class="team-info__logo">
      <h1 class="team-info__name">{{teamName}}</h1>
    </div>
    <hr class="team-info__divider"/>
    <div class="team-info__season-picker container-row">
      <season-picker type="team"/>
    </div>
    <div class="container-row">
      <team-main-stat v-for="el in ratings" :key="el.id"  v-bind="el"/>
    </div>
    <teams-stats-table type="team"/>
    <skaters-stats-table type="team"/>
    <goalies-stats-table type="team"/>
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
import {format} from 'd3-format';

let f1 = format('.1f');
let f2 = format('.2f');
let f3 = format('.3f');

export default {
  name: 'team-info',
  components: {TeamMainStat},
  props: {
  },
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
          awayStatistics: 'AWAY STATISTICS'
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
          awayStatistics: 'СТАТИСТИКА В ГОСТЕВЫХ ИГРАХ'
        }
      }
    }
  },
  data() {
    return {
      logoUrl: `images/team${this.$route.params.id}.svg`
    };
  },
  created() {
    this.requestTeamInfo();
  },
  computed: {
    teamName() {
      let teamInfo = this.$store.state.teams.teamSeasonInfo;
      if (!teamInfo.team) {
        return '';
      }
      return teamInfo.team.name;
    },

    ratings() {
      let selSeason = this.$store.state.season.selectedSeason;
      let teamInfo = this.$store.state.teams.teamSeasonInfo;
      if (this.needRequest(teamInfo, selSeason)) {
        this.requestTeamInfo();
        return [];
      }
      return [{
        id: 'goalsForPerGame',
        label: this.$t('statNames.goalsForPerGame'),
        value: teamInfo.goalsForPerGame,
        rating: teamInfo.goalsForPerGameRate,
        average: teamInfo.goalsForPerGameAvg
      }, {
        id: 'goalsAgainstPerGame',
        label: this.$t('statNames.goalsAgainstPerGame'),
        value: teamInfo.goalsAgainstPerGame,
        rating: teamInfo.goalsAgainstPerGameRate,
        average: teamInfo.goalsAgainstPerGameAvg,
        sortOrder: 'asc'
      }, {
        id: 'ppPercentage',
        label: this.$t('statNames.ppPercentage'),
        value: teamInfo.ppPercentage,
        rating: teamInfo.ppPercentageRate,
        average: teamInfo.ppPercentageAvg
      }, {
        id: 'pkPercentage',
        label: this.$t('statNames.pkPercentage'),
        value: teamInfo.pkPercentage,
        rating: teamInfo.pkPercentageRate,
        average: teamInfo.pkPercentageAvg
      }, {
        id: 'shootingPercentage',
        label: this.$t('statNames.shootingPercentage'),
        value: teamInfo.shootingPercentage,
        rating: teamInfo.shootingPercentageRate,
        average: teamInfo.shootingPercentageAvg
      }];
    },

    goalStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let teamInfo = this.$store.state.teams.teamSeasonInfo;
      if (this.needRequest(teamInfo, selSeason)) {
        this.requestTeamInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.goalsFor'),
        value: teamInfo.goalsFor
      }, {
        name: this.$t('statNames.goalsForPerGame'),
        value: teamInfo.goalsForPerGame,
        precision: f2
      }, {
        name: this.$t('statNames.goalsAgainst'),
        value: teamInfo.goalsAgainst
      }, {
        name: this.$t('statNames.goalsAgainstPerGame'),
        value: teamInfo.goalsAgainstPerGame,
        precision: f2
      }];
    },

    shootingStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let teamInfo = this.$store.state.teams.teamSeasonInfo;
      if (this.needRequest(teamInfo, selSeason)) {
        this.requestTeamInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.shotsPerGame'),
        value: teamInfo.shotsPerGame,
        precision: f1
      }, {
        name: this.$t('statNames.shotsAgainstPerGame'),
        value: teamInfo.shotsAgainstPerGame,
        precision: f1
      }, {
        name: this.$t('statNames.shootingPercentage'),
        value: teamInfo.shootingPercentage,
        precision: f2,
        percentage: true
      }, {
        name: this.$t('statNames.oppShootingPercentage'),
        value: teamInfo.oppShootingPercentage,
        precision: f2,
        percentage: true
      }];
    },

    advancedStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let teamInfo = this.$store.state.teams.teamSeasonInfo;
      if (this.needRequest(teamInfo, selSeason)) {
        this.requestTeamInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.scoringEfficiencyRatio'),
        value: teamInfo.scoringEfficiencyRatio,
        precision: f2
      }, {
        name: this.$t('statNames.shotEfficiencyRatio'),
        value: teamInfo.shotEfficiencyRatio,
        precision: f2
      }, {
        name: this.$t('statNames.penaltyEfficiencyRatio'),
        value: teamInfo.penaltyEfficiencyRatio,
        precision: f2
      }, {
        name: this.$t('statNames.pointsPerGame'),
        value: teamInfo.pointsPerGame,
        precision: f2
      }, {
        name: this.$t('statNames.faceOffWinsPercentage'),
        value: teamInfo.faceOffWinsPercentage,
        precision: f2,
        percentage: true
      }];
    },

    ppStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let teamInfo = this.$store.state.teams.teamSeasonInfo;
      if (this.needRequest(teamInfo, selSeason)) {
        this.requestTeamInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.ppPercentage'),
        value: teamInfo.ppPercentage,
        precision: f2,
        percentage: true
      }, {
        name: this.$t('statNames.ppGoals'),
        value: teamInfo.ppGoals
      }, {
        name: this.$t('statNames.ppGoalsPerGame'),
        value: teamInfo.ppGoalsPerGame,
        precision: f2
      }, {
        name: this.$t('statNames.ppPerGame'),
        value: teamInfo.ppPerGame,
        precision: f2
      }];
    },

    pkStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let teamInfo = this.$store.state.teams.teamSeasonInfo;
      if (this.needRequest(teamInfo, selSeason)) {
        this.requestTeamInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.pkPercentage'),
        value: teamInfo.pkPercentage,
        precision: f2,
        percentage: true
      }, {
        name: this.$t('statNames.shGoalsAgainst'),
        value: teamInfo.shGoalsAgainst
      }, {
        name: this.$t('statNames.shGoalsAgainstPerGame'),
        value: teamInfo.shGoalsAgainstPerGame,
        precision: f2
      }, {
        name: this.$t('statNames.shPerGame'),
        value: teamInfo.shPerGame,
        precision: f2
      }];
    },

    goaltenderStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let teamInfo = this.$store.state.teams.teamSeasonInfo;
      if (this.needRequest(teamInfo, selSeason)) {
        this.requestTeamInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.savePercentage'),
        value: teamInfo.savePercentage,
        precision: f3
      }, {
        name: this.$t('statNames.oppSavePercentage'),
        value: teamInfo.oppSavePercentage,
        precision: f3
      }, {
        name: this.$t('statNames.shutouts'),
        value: teamInfo.shutouts
      }];
    },

    homeStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let teamInfo = this.$store.state.teams.teamSeasonInfo;
      if (this.needRequest(teamInfo, selSeason)) {
        this.requestTeamInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.goalsFor'),
        value: teamInfo.homeGoals
      }, {
        name: this.$t('statNames.goalsAgainst'),
        value: teamInfo.homeGoalsAgainst
      }, {
        name: this.$t('statNames.shots'),
        value: teamInfo.homeShots
      }, {
        name: this.$t('statNames.shotsAgainst'),
        value: teamInfo.homeShotsAgainst
      }, {
        name: this.$t('statNames.ppPercentage'),
        value: teamInfo.homePPPercentage,
        precision: f2,
        percentage: true
      }, {
        name: this.$t('statNames.pkPercentage'),
        value: teamInfo.homePKPercentage,
        precision: f2,
        percentage: true
      }];
    },

    awayStats() {
      let selSeason = this.$store.state.season.selectedSeason;
      let teamInfo = this.$store.state.teams.teamSeasonInfo;
      if (this.needRequest(teamInfo, selSeason)) {
        this.requestTeamInfo();
        return [];
      }
      return [{
        name: this.$t('statNames.goalsFor'),
        value: teamInfo.awayGoals
      }, {
        name: this.$t('statNames.goalsAgainst'),
        value: teamInfo.awayGoalsAgainst
      }, {
        name: this.$t('statNames.shots'),
        value: teamInfo.awayShots
      }, {
        name: this.$t('statNames.shotsAgainst'),
        value: teamInfo.awayShotsAgainst
      }, {
        name: this.$t('statNames.ppPercentage'),
        value: teamInfo.awayPPPercentage,
        precision: f2,
        percentage: true
      }, {
        name: this.$t('statNames.pkPercentage'),
        value: teamInfo.awayPKPercentage,
        precision: f2,
        percentage: true
      }];
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

    needRequest(teamInfo, selSeason) {
      return !teamInfo.team || teamInfo.team.id !== parseInt(this.$route.params.id) ||
             selSeason.id !== teamInfo.season.id || selSeason.regular !== teamInfo.season.regular;
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
  .team-info__season-picker {
    justify-content: flex-end;
    padding: 0 2rem;
    margin: 1rem 0;
  }
  .team-info__divider {
    background: @border-color;
    height: .25rem;
    width: 95%;
    margin: 1rem 2.5%;
    border: none;
  }
</style>
