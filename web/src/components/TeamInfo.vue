<template>
  <div class="team-info">
    <img :src="logoUrl" class="team-info__logo">
    <season-picker type="all"></season-picker>
    <div class="container-row">
      <team-main-stat v-for="el in ratings"
        :key="el.id" :label="el.label" :value="el.value" :rating="el.rate" :average="el.avg" :sortOrder="el.sortOrder">
      </team-main-stat>
    </div>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import TeamMainStat from 'Components/TeamMainStat';
import SeasonPicker from 'Components/SeasonPicker';

export default {
  name: 'team-info',
  components: {TeamMainStat, SeasonPicker},
  props: {
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
    ratings() {
      let selSeason = this.$store.state.season.selectedSeason;
      let teamInfo = this.$store.state.teams.teamSeasonInfo;
      if (!teamInfo.team || selSeason.id !== teamInfo.season.id || selSeason.regular !== teamInfo.season.regular) {
        this.requestTeamInfo();
        return [];
      }
      return [{
          id: 'goalsForPerGame',
          label: this.$t('statNames.goalsForPerGame'),
          value: teamInfo.goalsForPerGame,
          rate: teamInfo.goalsForPerGameRate,
          avg: teamInfo.goalsForPerGameAvg
        }, {
          id: 'goalsAgainstPerGame',
          label: this.$t('statNames.goalsAgainstPerGame'),
          value: teamInfo.goalsAgainstPerGame,
          rate: teamInfo.goalsAgainstPerGameRate,
          avg: teamInfo.goalsAgainstPerGameAvg,
          sortOrder: 'asc'
        }, {
          id: 'ppPercentage',
          label: this.$t('statNames.ppPercentage'),
          value: teamInfo.ppPercentage,
          rate: teamInfo.ppPercentageRate,
          avg: teamInfo.ppPercentageAvg
        }, {
          id: 'pkPercentage',
          label: this.$t('statNames.pkPercentage'),
          value: teamInfo.pkPercentage,
          rate: teamInfo.pkPercentageRate,
          avg: teamInfo.pkPercentageAvg
        }, {
          id: 'shootingPercentage',
          label: this.$t('statNames.shootingPercentage'),
          value: teamInfo.shootingPercentage,
          rate: teamInfo.shootingPercentageRate,
          avg: teamInfo.shootingPercentageAvg
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
    }
  }
};

</script>

<style lang="less">
  .team-info__logo {
    width: 200px;
    height: 200px;
  }
</style>
