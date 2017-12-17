<template>
  <div class="">
    <div class="container-row">
      <leaders-preview type="skaterGoal"></leaders-preview>
      <leaders-preview type="skaterAssist"></leaders-preview>
      <leaders-preview type="skaterPoint"></leaders-preview>
      <leaders-preview type="skaterPlusMinus"></leaders-preview>
      <leaders-preview type="goalieGaa"></leaders-preview>
      <leaders-preview type="goalieSavePercentage"></leaders-preview>
    </div>
    <div class="container-row">
      <standings num="1"></standings>
      <standings num="2"></standings>
    </div>
  </div>
</template>

<script>
import LeadersPreview from 'Components/LeadersPreview';
import Standings from 'Components/Standings';

export default {
  name: 'home',
  components: {LeadersPreview, Standings},
  props: {},
  data() {
    return {};
  },
  computed: {},
  methods: {}
};

</script>

<style lang="less">
</style>
