<template>
  <div class="">
    <team-picker/>
    <season-picker type="all"/>
    <teams-stats-table type="all"/>
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
