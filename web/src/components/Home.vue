<template>
  <div class="">
    <h1>This is Home page.</h1>
    <leaders-preview type="goal"></leaders-preview>
  </div>
</template>

<script>
import LeadersPreview from 'Components/LeadersPreview';
import {SeasonRequestParams} from 'Store/types';

export default {
  name: 'home',
  components: {LeadersPreview},
  props: {},
  data() {
    return {};
  },
  created() {
    this.$store.dispatch('getSkatersStats', {reqParams: new SeasonRequestParams(this.$store)});
  },
  computed: {},
  methods: {}
};

</script>

<style lang="less">
</style>
