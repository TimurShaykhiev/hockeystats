<template>
  <div class="preview-table">
    <table>
      <caption>{{$t(type)}}</caption>
      <tr v-for="elem in dataSet">
        <td>{{elem.name}}</td>
        <td>{{elem.value}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';

const ITEMS_TO_SHOW = 10;

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
        skaterPoint: 'Points'
      },
      ru: {
        skaterGoal: 'Голы',
        skaterAssist: 'Пасы',
        skaterPoint: 'Очки'
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
      allStats.sort((a, b) => {
        if (getValueFunc(a) > getValueFunc(b)) {
          return -1;
        }
        if (getValueFunc(a) < getValueFunc(b)) {
          return 1;
        }
        return 0;
      });
      let statsToShow;
      if (typesMap[this.type].descSort) {
        statsToShow = allStats.slice(0, ITEMS_TO_SHOW);
      } else {
        statsToShow = allStats.slice(allStats.length-ITEMS_TO_SHOW).reverse();
      }
      return statsToShow.map((x) => {
        return {name: x.player.name, value: getValueFunc(x)};
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
        width: 40px;
        text-align: center;
      }
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
</style>
