<template>
  <div class="team-picker">
    <button class="button button--green" @click="toggleTeamsView">{{$t('teamPickerButtonLabel')}}</button>
    <div v-if="showTeams" class="team-picker__container">
      <div class="container-row">
        <div v-for="el in divisions" class="team-picker__div-container container-col">
          <h3 class="team-picker__div-name">{{el.name}}</h3>
          <div v-for="team in teams[el.id]" class="team-picker__team">
            {{team.name}}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import Utils from 'Root/utils';

export default {
  name: 'team-picker',
  props: {
  },
  i18n: {
    messages: {
      en: {
        teamPickerButtonLabel: 'Teams'
      },
      ru: {
        teamPickerButtonLabel: 'Команды'
      }
    }
  },
  data() {
    return {
      showTeams: true
    };
  },
  created() {
    let season = this.$store.state.season.selectedSeason;
    if (season.id !== undefined) {
      this.$store.dispatch('getTeamStats', {
        reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
      });
    }
  },
  computed: {
    divisions() {
      let divisions = this.$store.state.teams.divisions;
      if (divisions.length === 0) {
        return [];
      }
      return divisions;
    },

    teams() {
      let divisions = this.$store.state.teams.divisions;
      let teamStats = this.$store.state.teams.teamStats.teams;
      if (divisions.length === 0 || !teamStats) {
        return {};
      }
      let teams = {};
      for (let d of divisions) {
        let divTeams = teamStats.filter((t) => t.team.did === d.id);
        let arr = divTeams.map((t) => {
          return {id: t.team.id, name: this.$t(`teams.${t.team.id}`)};
        });
        teams[d.id] = Utils.sortBy(arr, (e) => e.name);
      }
      return teams;
    }
  },
  methods: {
    toggleTeamsView() {
      this.showTeams = !this.showTeams;
    }
  }
};

</script>

<style lang="less">
  .team-picker {
    margin-bottom: 20px;
  }
  .team-picker__container {
    border: 1px solid slategrey;
    border-radius: 10px;
    background: slategrey;
  }
  .team-picker__div-container {
    margin: 10px 20px;
  }
  .team-picker__div-name {
    color: white;
  }
  .team-picker__team {
    margin: 3px 0;
    color: lightgrey;
    &:hover {
      color: white;
    }
  }
</style>
