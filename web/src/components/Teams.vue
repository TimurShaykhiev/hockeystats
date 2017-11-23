<template>
  <div class="">
    <season-picker type="all"></season-picker>
    <h1>This is Teams page.</h1>
  </div>
</template>

<script>
import SeasonPicker from 'Components/SeasonPicker';

export default {
  name: 'teams',
  components: {SeasonPicker},
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
