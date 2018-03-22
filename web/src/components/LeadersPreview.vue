<template>
  <div class="preview-table">
    <table>
      <caption>{{$t(type)}}</caption>
      <tr v-for="elem in dataSet">
        <td>
          <router-link :to="{name: elem.routeName, params: {id: elem.pid}}">{{elem.name}}</router-link>
          <span class="preview-table__team-name">{{elem.team}}</span>
        </td>
        <td>{{elem.value}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import CompUtils from 'Components/utils';
import {format} from 'd3-format';

const ITEMS_TO_SHOW = 5;
let GAMES_LIMIT = 5;

let f2 = format('.2f');

const typesMap = {
  skaterGoal: {
    action: 'getSkaterStats',
    getStats: 'skaterStats',
    setLimits: 'setSkaterStatsLimits',
    routeName: 'skater',
    getValue: (plStats) => plStats.stats.goals,
    descSort: true
  },
  skaterAssist: {
    action: 'getSkaterStats',
    getStats: 'skaterStats',
    setLimits: 'setSkaterStatsLimits',
    routeName: 'skater',
    getValue: (plStats) => plStats.stats.assists,
    descSort: true
  },
  skaterPoint: {
    action: 'getSkaterStats',
    getStats: 'skaterStats',
    setLimits: 'setSkaterStatsLimits',
    routeName: 'skater',
    getValue: (plStats) => plStats.stats.goals + plStats.stats.assists,
    descSort: true
  },
  skaterPlusMinus: {
    action: 'getSkaterStats',
    getStats: 'skaterStats',
    setLimits: 'setSkaterStatsLimits',
    routeName: 'skater',
    getValue: (plStats) => plStats.stats.plusMinus,
    descSort: true
  },
  goalieGaa: {
    action: 'getGoalieStats',
    getStats: 'goalieStats',
    setLimits: 'setGoalieStatsLimits',
    routeName: 'goalie',
    getValue: (plStats) => plStats.stats.games >= GAMES_LIMIT ? plStats.stats.gaa : 1000,
    showValue: (value) => f2(value),
    descSort: false
  },
  goalieSavePercentage: {
    action: 'getGoalieStats',
    getStats: 'goalieStats',
    setLimits: 'setGoalieStatsLimits',
    routeName: 'goalie',
    getValue: (plStats) => plStats.stats.games >= GAMES_LIMIT ? plStats.stats.svp : 0,
    showValue: (value) => CompUtils.omitInteger(value, 3),
    descSort: true
  }
};

export default {
  name: 'leaders-preview',
  props: {
    type: {type: String, required: true}
  },
  i18n: {
    messages: {
      en: {
        skaterGoal: 'Goals',
        skaterAssist: 'Assists',
        skaterPoint: 'Points',
        skaterPlusMinus: 'Plus-Minus',
        goalieGaa: 'Goals Against Average',
        goalieSavePercentage: 'Save Percentage'
      },
      ru: {
        skaterGoal: 'Голы',
        skaterAssist: 'Пасы',
        skaterPoint: 'Очки',
        skaterPlusMinus: 'Плюс-Минус',
        goalieGaa: 'Коэф. надёжности',
        goalieSavePercentage: '%ОБ'
      }
    }
  },
  data() {
    return {};
  },
  created() {
    this.$store.dispatch('getCurrentSeason').then((season) => {
      this.$store.dispatch('getAllTeams', {
        reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
      });
      this.$store.dispatch(typesMap[this.type].action, {
        reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
      });
    });
  },
  computed: {
    dataSet() {
      let allTeams = this.$store.state.teams.allTeams.teams;
      let allStats = this[typesMap[this.type].getStats]();
      if (!allTeams || !allStats) {
        return [];
      }
      this[typesMap[this.type].setLimits]();
      allStats = allStats.slice();
      let getValueFunc = typesMap[this.type].getValue;
      let showValueFunc = typesMap[this.type].showValue;
      allStats.sort((a, b) => {
        let valueA = getValueFunc(a);
        let valueB = getValueFunc(b);
        if (valueA > valueB) return -1;
        if (valueA < valueB) return 1;
        // The fewer games played, the higher in chart.
        if (a.games > b.games) return 1;
        if (a.games < b.games) return -1;
        return 0;
      });
      let statsToShow;
      if (typesMap[this.type].descSort) {
        statsToShow = allStats.slice(0, ITEMS_TO_SHOW);
      } else {
        statsToShow = allStats.slice(allStats.length-ITEMS_TO_SHOW).reverse();
      }
      const routeName = typesMap[this.type].routeName;
      return statsToShow.map((x) => {
        return {
          pid: x.player.id,
          name: x.player.name,
          routeName: routeName,
          team: allTeams[x.player.tid].name,
          value: showValueFunc ? showValueFunc(getValueFunc(x)) : getValueFunc(x)
        };
      });
    }
  },
  methods: {
    skaterStats() {
      return this.$store.state.players.skaterStats.skaters;
    },
    goalieStats() {
      return this.$store.state.players.goalieStats.goalies;
    },
    setSkaterStatsLimits() {
    },
    setGoalieStatsLimits() {
      this.$store.dispatch('getGoalieStatsLimits', {season: this.$store.state.season.currentSeason});
      GAMES_LIMIT = this.$store.state.players.goalieStatsLimits.limits.games;
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .preview-table {
    margin: .75rem;
    table {
      border-collapse: collapse;
      border: 1px solid @border-color;
      width: 16rem;
      table-layout: fixed;
    }
    caption {
      height: 2em;
      color: @header-text-color;
      background: @header-color;
      line-height: 2em;
      font-size: 1.3rem;
    }
    tr {
      height: 3em;
      &:nth-of-type(odd) {
        background-color: @table-striped-color;
      }
    }
    td {
      padding: 0 .6rem;
      &:nth-of-type(even) {
        width: 3rem;
        text-align: center;
      }
      overflow: hidden;
      text-overflow: ellipsis;
      a {
        display: block;
        color: black;
        text-decoration: none;
      }
      .preview-table__team-name {
        font-size: .75rem;
      }
    }
  }
</style>
