<template>
  <div class="">
    <team-picker/>
    <season-picker type="all"/>
    <teams-stats-table type="all"/>
  </div>
</template>

<script>
import TeamPicker from 'Components/TeamPicker';

export default {
  name: 'teams',
  components: {TeamPicker},
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
