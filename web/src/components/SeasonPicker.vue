<template>
  <div class="season-picker container-row">
    <h4 class="season-picker__label">{{$t("seasonLabel")}}</h4>
    <select class="season-picker__select" v-model="selectedSeason" @change="seasonChanged">
      <option v-for="el in seasonsList" :value="el.value">{{el.name}}</option>
    </select>
  </div>
</template>

<script>

export default {
  name: 'season-picker',
  props: {
    type: {type: String, required: true}
  },
  i18n: {
    messages: {
      en: {
        seasonLabel: 'Season',
        playoffLabel: 'Playoff'
      },
      ru: {
        seasonLabel: 'Сезон',
        playoffLabel: 'Плей-офф'
      }
    }
  },
  data() {
    return {
      // for playoff season id is negative
      selectedSeason: null
    };
  },
  created() {
    if (this.type === 'all') {
      this.$store.dispatch('getAllSeasons').then((result) => {
        this.setSelectedSeason(result.seasons);
      });
    } else if (this.type === 'team') {
      this.$store.dispatch('getTeamSeasons', {teamId: this.$route.params.id}).then((result) => {
        this.setSelectedSeason(result.seasons);
      });
    } else if (this.type === 'skater') {
      this.$store.dispatch('getSkaterSeasons', {teamId: this.$route.params.id}).then((result) => {
        this.setSelectedSeason(result.seasons);
      });
    } else if (this.type === 'goalie') {
      this.$store.dispatch('getGoalieSeasons', {teamId: this.$route.params.id}).then((result) => {
        this.setSelectedSeason(result.seasons);
      });
    }
  },
  computed: {
    seasonsList() {
      let seasons = this.getSeasons();
      if (seasons === undefined) {
        return [];
      }
      let result = [];
      for (let el of seasons) {
        let name;
        let id;
        if (el.regular) {
          name = `${el.year}-${el.year % 100 + 1}`;
          id = el.id;
        } else {
          name = `${el.year}-${el.year % 100 + 1} ${this.$t('playoffLabel')}`;
          id = -el.id;
        }
        result.push({name: name, value: id});
      }
      return result;
    }
  },
  methods: {
    getSeasons() {
      if (this.type === 'all') {
        return this.$store.state.season.allSeasons.seasons;
      } else if (this.type === 'team') {
        return this.$store.state.teams.teamSeasons.seasons;
      } else if (this.type === 'skater') {
        return this.$store.state.players.skaterSeasons.seasons;
      } else if (this.type === 'goalie') {
        return this.$store.state.players.goalieSeasons.seasons;
      }
    },
    seasonChanged() {
      this.$store.commit('setSelectedSeason', {id: Math.abs(this.selectedSeason), regular: this.selectedSeason > 0});
    },
    setSelectedSeason(seasons) {
      let selectedSeason = this.$store.state.season.selectedSeason;
      if (selectedSeason.id !== undefined &&
          seasons.find((el) => el.id === selectedSeason.id) !== undefined) {
        // Set selected season from storage
        this.selectedSeason = selectedSeason.regular ? selectedSeason.id : -selectedSeason.id;
      } else {
        // Not in storage yet or seasons list does not contain selected season.
        // Set first season in list as selected.
        this.selectedSeason = seasons[0].regular ? seasons[0].id : -seasons[0].id;
        this.seasonChanged();
      }
    }
  }
};

</script>

<style lang="less">
  .season-picker {
    font-size: 1.2rem;
  }
  .season-picker__label {
    margin: 0 .8rem;
  }
  .season-picker__select {
    border-radius: 4px;
  }
</style>
