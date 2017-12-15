<template>
  <div class="">
    <season-picker type="all"></season-picker>
    <skaters-stats-table></skaters-stats-table>
  </div>
</template>

<script>
import SeasonPicker from 'Components/SeasonPicker';
import SkatersStatsTable from 'Components/SkatersStatsTable';

export default {
  name: 'skaters',
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
