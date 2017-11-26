<template>
  <div class="season-picker">
    <label>{{$t("seasonLabel")}}
      <select v-model="selectedSeason" @change="seasonChanged">
        <option v-for="el in seasonsList" :value="el.value">{{el.name}}</option>
      </select>
    </label>
    <toggle-button v-model="isRegular"
                   :labels="labels"
                   :color="{checked: '#7DCE94', unchecked: '#82C7EB'}"
                   :width="100"
                   @change="seasonChanged">
    </toggle-button>
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
        regularLabel: 'Regular',
        playoffLabel: 'Playoff'
      },
      ru: {
        seasonLabel: 'Сезон',
        regularLabel: 'Регулярный',
        playoffLabel: 'Плей-офф'
      }
    }
  },
  data() {
    return {
      labels: {checked: this.$t('regularLabel'), unchecked: this.$t('playoffLabel')},
      selectedSeason: '',
      isRegular: true
    };
  },
  created() {
    if (this.type === 'all') {
      this.$store.dispatch('getAllSeasons').then((result) => {
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
        result.push({name: `${el.year}-${el.year % 100 + 1}`, value: el.id});
      }
      return result;
    }
  },
  methods: {
    getSeasons() {
      if (this.type === 'all') {
        return this.$store.state.season.allSeasons.seasons;
      }
    },
    seasonChanged() {
      this.$store.commit('setSelectedSeason', {id: this.selectedSeason, regular: this.isRegular});
    },
    setSelectedSeason(seasons) {
      let selectedSeason = this.$store.state.season.selectedSeason;
      if (selectedSeason.id !== undefined &&
          seasons.find((el) => el.id === selectedSeason.id) !== undefined) {
        // Set selected season from storage
        this.selectedSeason = selectedSeason.id;
        this.isRegular = selectedSeason.regular;
      } else {
        // Not in storage yet or seasons list does not contain selected season.
        // Set first season in list as selected.
        this.selectedSeason = seasons[0].id;
        this.seasonChanged();
      }
    }
  }
};

</script>

<style lang="less">
</style>
