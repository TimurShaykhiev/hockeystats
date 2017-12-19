<template>
  <div class="team-info">
    <img :src="logoUrl" class="team-info__logo">
    <h2>{{name}}</h2>
  </div>
</template>

<script>

export default {
  name: 'team-info',
  props: {
  },
  data() {
    return {
      name: this.$t(`teams.${this.$route.params.id}`),
      logoUrl: `images/team${this.$route.params.id}.svg`
    };
  },
  created() {
  },
  computed: {
  },
  methods: {
  }
};

</script>

<style lang="less">
  .team-info__logo {
    width: 200px;
    height: 200px;
  }
</style>
