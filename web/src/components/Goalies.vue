<template>
  <div class="">
    <season-picker type="all"></season-picker>
    <goalies-stats-table></goalies-stats-table>
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
