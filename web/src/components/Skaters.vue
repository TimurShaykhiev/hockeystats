<template>
  <div class="">
    <season-picker type="all"/>
    <skaters-stats-table type="all"/>
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
