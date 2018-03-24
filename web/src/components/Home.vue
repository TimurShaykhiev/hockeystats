<template>
  <div class="home">
    <h2 class="home__season-name">{{seasonName}}</h2>
    <div class="home__leader-preview-container container-row">
      <leaders-preview type="skaterGoal"></leaders-preview>
      <leaders-preview type="skaterAssist"></leaders-preview>
      <leaders-preview type="skaterPoint"></leaders-preview>
      <leaders-preview type="skaterPlusMinus"></leaders-preview>
      <leaders-preview type="goalieGaa"></leaders-preview>
      <leaders-preview type="goalieSavePercentage"></leaders-preview>
    </div>
    <div class="home__standings-container container-row">
      <standings num="1"></standings>
      <standings num="2"></standings>
    </div>
  </div>
</template>

<script>
import LeadersPreview from 'Components/LeadersPreview';
import Standings from 'Components/Standings';
import CompUtils from 'Components/utils';

export default {
  name: 'home',
  components: {LeadersPreview, Standings},
  computed: {
    seasonName() {
      let season = this.$store.state.season.currentSeason;
      if (season.id !== undefined) {
        return CompUtils.seasonToStr(season);
      }
      return '';
    }
  }
};

</script>

<style lang="less">
  .home__season-name {
    text-align: center;
    margin: 1rem 0;
  }
  .home__leader-preview-container {
    justify-content: space-evenly;
  }
  .home__standings-container {
    justify-content: space-around;
    margin-top: 2rem;
  }
</style>
