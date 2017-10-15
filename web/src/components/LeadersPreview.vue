<template>
  <div class="">
    <table>
      <tr v-for="elem in dataSet">
        <td>{{elem.name}}</td>
        <td>{{elem.value}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';

const ITEMS_TO_SHOW = 5;

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
  data() {
    return {};
  },
  created() {
    this.$store.dispatch(typesMap[this.type].action, {reqParams: new SeasonRequestParams(this.$store)});
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
</style>
