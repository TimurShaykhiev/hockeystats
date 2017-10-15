<template>
  <div class="">
    <table>
      <tr v-for="elem in dataSet">
        <td>{{elem.player.name}}</td>
        <td>{{elem.stats.goals}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';

export default {
  name: 'leaders-preview',
  props: {
    type: {type: String, required: true}
  },
  data() {
    return {};
  },
  created() {
    this.$store.dispatch('getSkatersStats', {reqParams: new SeasonRequestParams(this.$store)});
  },
  computed: {
    dataSet() {
      return this.$store.state.players.skaterStats.skaters;
    }
  },
  methods: {
  }
};

</script>

<style lang="less">
</style>
