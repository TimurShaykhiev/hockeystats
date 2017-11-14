<template>
  <div class="preview-table">
    <table>
      <caption>{{$t(type)}}</caption>
      <tr v-for="elem in dataSet">
        <td>
          <span class="preview-table__player-name">{{elem.name}}</span>
          <span class="preview-table__team-name">{{elem.team}}</span>
        </td>
        <td>{{elem.value}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import {floatToStr} from 'Components/utils';

const ITEMS_TO_SHOW = 5;
const GAMES_MIN_LIMIT = 5;

const typesMap = {
  skaterGoal: {
    action: 'getSkaterStats',
    getStats: 'skaterStats',
    getValue: (plStats) => plStats.stats.goals,
    descSort: true
  },
  skaterAssist: {
    action: 'getSkaterStats',
    getStats: 'skaterStats',
    getValue: (plStats) => plStats.stats.assists,
    descSort: true
  },
  skaterPoint: {
    action: 'getSkaterStats',
    getStats: 'skaterStats',
    getValue: (plStats) => plStats.stats.goals + plStats.stats.assists,
    descSort: true
  },
  skaterPlusMinus: {
    action: 'getSkaterStats',
    getStats: 'skaterStats',
    getValue: (plStats) => plStats.stats.plusMinus,
    descSort: true
  },
  goalieGaa: {
    action: 'getGoalieStats',
    getStats: 'goalieStats',
    getValue: (plStats) => plStats.stats.games >= GAMES_MIN_LIMIT ? plStats.stats.gaa : 1000,
    showValue: (value) => floatToStr(value, 2),
    descSort: false
  },
  goalieSavePercentage: {
    action: 'getGoalieStats',
    getStats: 'goalieStats',
    getValue: (plStats) => plStats.stats.games >= GAMES_MIN_LIMIT ? plStats.stats.svp : 0,
    showValue: (value) => floatToStr(value, 3, true),
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
        goalieSavePercentage: '% ОБ'
      }
    }
  },
  data() {
    return {};
  },
  created() {
    this.$store.dispatch('getCurrentSeason').then((season) => {
      this.$store.dispatch(typesMap[this.type].action, {
        reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
      });
    });
  },
  computed: {
    dataSet() {
      let allStats = this[typesMap[this.type].getStats]();
      if (allStats === undefined) {
        return [];
      }
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
      return statsToShow.map((x) => {
        return {
          name: x.player.name,
          team: this.$t(`teams.${x.player.tid}`),
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
    }
  }
};

</script>

<style lang="less">
  .preview-table {
    margin: 10px;
    table {
      border-collapse: collapse;
      border: 1px solid black;
      width: 250px;
      table-layout: fixed;
    }
    caption {
      height: 2em;
      color: white;
      background: black;
      line-height: 2em;
      font-size: 1.3em;
    }
    tr {
      height: 2em;
      &:first-of-type {
        height: 3em;
        font-size: 1.5em;
      }
      &:nth-of-type(odd) {
        background: #e1e1e1;
      }
    }
    td {
      padding: 0 10px;
      &:nth-of-type(even) {
        width: 50px;
        text-align: center;
      }
      overflow: hidden;
      text-overflow: ellipsis;
      span {
        &.preview-table__player-name {
          display: block;
        }
        &.preview-table__team-name {
          font-size: 12px;
        }
      }
    }
  }
</style>
