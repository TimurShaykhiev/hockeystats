<template>
  <div class="">
    <season-picker type="all"/>
    <goalies-stats-table type="all"/>
  </div>
</template>

<script>
import SeasonPicker from 'Components/SeasonPicker';
import GoaliesStatsTable from 'Components/GoaliesStatsTable';

export default {
  name: 'goalies',
  components: {SeasonPicker, GoaliesStatsTable},
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
