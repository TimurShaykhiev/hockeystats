<template>
  <div class="">
    <season-picker type="all"></season-picker>
    <h1>This is Teams page.</h1>
    <teams-stats-table></teams-stats-table>
  </div>
</template>

<script>
import SeasonPicker from 'Components/SeasonPicker';
import TeamsStatsTable from 'Components/TeamsStatsTable';

export default {
  name: 'teams',
  components: {SeasonPicker, TeamsStatsTable},
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
