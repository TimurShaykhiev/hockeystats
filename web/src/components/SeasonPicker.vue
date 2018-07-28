<template>
  <div class="season-picker container-row">
    <h4 class="season-picker__label">{{$t("seasonLabel")}}</h4>
    <select class="season-picker__select" v-model="selectedSeason" @change="seasonChanged">
      <option v-for="el in seasonsList" :value="el.value">{{el.name}}</option>
    </select>
  </div>
</template>

<script>

const TYPE_ALL = 'all';
const TYPE_TEAM = 'team';
const TYPE_SKATER = 'skater';
const TYPE_GOALIE = 'goalie';
const TYPE_ALL_FINISHED = 'all-finished';

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
    if (this.type === TYPE_ALL || this.type === TYPE_ALL_FINISHED) {
      this.$store.dispatch('getAllSeasons').then((result) => {
        this.setSelectedSeason(result.seasons);
      });
    } else if (this.type === TYPE_TEAM) {
      this.$store.dispatch('getTeamSeasons', {teamId: this.$route.params.id}).then((result) => {
        this.setSelectedSeason(result.seasons);
      });
    } else if (this.type === TYPE_SKATER) {
      this.$store.dispatch('getSkaterSeasons', {playerId: this.$route.params.id}).then((result) => {
        this.setSelectedSeason(result.seasons);
      });
    } else if (this.type === TYPE_GOALIE) {
      this.$store.dispatch('getGoalieSeasons', {playerId: this.$route.params.id}).then((result) => {
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
        if (!this.isSeasonValid(el)) {
          continue;
        }
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
      if (this.type === TYPE_ALL || this.type === TYPE_ALL_FINISHED) {
        return this.$store.state.season.allSeasons.seasons;
      } else if (this.type === TYPE_TEAM) {
        return this.$store.state.teams.teamSeasons.seasons;
      } else if (this.type === TYPE_SKATER) {
        return this.$store.state.players.skaterSeasons.seasons;
      } else if (this.type === TYPE_GOALIE) {
        return this.$store.state.players.goalieSeasons.seasons;
      }
    },

    findSelectedSeason() {
      let seasons = this.getSeasons();
      let id = Math.abs(this.selectedSeason);
      let regular = this.selectedSeason > 0;
      return seasons.find((s) => s.id === id && s.regular === regular);
    },

    seasonChanged() {
      this.$store.commit('setSelectedSeason', this.findSelectedSeason());
    },

    setSelectedSeason(seasons) {
      let selectedSeason = this.$store.state.season.selectedSeason;
      if (selectedSeason.id !== undefined &&
          seasons.find((el) => {
            return el.id === selectedSeason.id && el.regular === selectedSeason.regular && this.isSeasonValid(el);
          }) !== undefined) {
        // Set selected season from storage
        this.selectedSeason = selectedSeason.regular ? selectedSeason.id : -selectedSeason.id;
      } else {
        // Not in storage yet or seasons list does not contain selected season.
        // Set first season in list as selected.
        for (let s of seasons) {
          if (this.isSeasonValid(s)) {
            this.selectedSeason = s.regular ? s.id : -s.id;
            break;
          }
        }
        this.seasonChanged();
      }
    },

    isSeasonValid(season) {
      let now = Date.now();
      return !(this.type === TYPE_ALL_FINISHED &&
        (season.regular && now < season.poStart || !season.regular && now < season.end));
    }
  }
};

</script>

<style lang="less">
  .season-picker {
    font-size: 1.2rem;
    height: 1.5rem;
  }
  .season-picker__label {
    margin: 0 .8rem;
  }
  .season-picker__select {
    border-radius: 4px;
    font-size: .9rem;
  }
</style>
