<template>
  <div class="">
    <h1>This is Home page.</h1>
    <div class="container-row">
      <leaders-preview type="skaterGoal"></leaders-preview>
      <leaders-preview type="skaterAssist"></leaders-preview>
      <leaders-preview type="skaterPoint"></leaders-preview>
    </div>
  </div>
</template>

<script>
import LeadersPreview from 'Components/LeadersPreview';

export default {
  name: 'home',
  components: {LeadersPreview},
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
