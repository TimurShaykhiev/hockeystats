<template>
  <div class="team-picker">
    <button class="button button--green" @click="toggleTeamsView">{{$t('teamPickerButtonLabel')}}</button>
    <div v-if="showTeams" class="team-picker__container">
      <div class="container-row">
        <div v-for="el in divisions" class="team-picker__div-container container-col">
          <h3 class="team-picker__div-name">{{el.name}}</h3>
          <div v-for="team in teams[el.id]" class="team-picker__team">
            <router-link :to="{name: 'team', params: {id: team.id}}">{{team.name}}</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {LocaleRequestParams} from 'Store/types';
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
      showTeams: false
    };
  },
  created() {
    this.$store.dispatch('getAllTeams', {reqParams: new LocaleRequestParams(this.$store)});
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
      let allTeams = this.$store.state.teams.allTeams.teams;
      if (divisions.length === 0 || !allTeams) {
        return {};
      }
      let teams = {};
      for (let d of divisions) {
        let divTeams = [];
        for (let key of Object.keys(allTeams)) {
          if (allTeams[key].did === d.id) {
            divTeams.push({id: allTeams[key].id, name: allTeams[key].name});
          }
        }
        teams[d.id] = Utils.sortBy(divTeams, (e) => e.name);
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
    a {
      color: lightgrey;
      text-decoration: none;
      &:hover {
        color: white;
      }
    }
  }
</style>
