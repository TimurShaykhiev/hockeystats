<template>
  <div class="">
    <season-picker type="all"></season-picker>
    <h1>This is Players page.</h1>
    <skaters-stats-table></skaters-stats-table>
  </div>
</template>

<script>
import SeasonPicker from 'Components/SeasonPicker';
import SkatersStatsTable from 'Components/SkatersStatsTable';

export default {
  name: 'players',
  components: {SeasonPicker, SkatersStatsTable},
  props: {
  },
  data() {
    return {};
  },
  computed: {
  },
  methods: {
  }
};

</script>

<style lang="less">
</style>
