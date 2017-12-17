<template>
  <div class="">
    <team-picker></team-picker>
    <season-picker type="all"></season-picker>
    <teams-stats-table></teams-stats-table>
  </div>
</template>

<script>
import SeasonPicker from 'Components/SeasonPicker';
import TeamsStatsTable from 'Components/TeamsStatsTable';
import TeamPicker from 'Components/TeamPicker';

export default {
  name: 'teams',
  components: {SeasonPicker, TeamsStatsTable, TeamPicker},
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
