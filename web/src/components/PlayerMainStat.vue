<template>
  <div class="player-main-stat container-col">
    <h1 class="player-main-stat__value">{{statValue}}</h1>
    <h3 class="player-main-stat__caption">{{caption}}</h3>
    <div class="player-main-stat__rating-block">
      <h2 class="player-main-stat__rating">{{placeInTotalRate}}</h2>
      <h3 class="player-main-stat__caption">{{$t('overall')}}</h3>
    </div>
    <div class="player-main-stat__rating-block" v-if="teamRating">
      <h2 class="player-main-stat__rating">{{placeInTeamRate}}</h2>
      <h3 class="player-main-stat__caption">{{$t('inTeam')}}</h3>
    </div>
  </div>
</template>

<script>
import {numberToOrdinal} from 'Components/utils';

export default {
  name: 'player-main-stat',
  props: {
    label: {type: String, required: true},
    value: {type: Number, required: true},
    precision: {type: Function},
    rating: {type: Number, required: true},
    teamRating: {type: Number}
  },
  i18n: {
    messages: {
      en: {
        overall: 'OVERALL',
        inTeam: 'IN TEAM'
      },
      ru: {
        overall: 'В ЛИГЕ',
        inTeam: 'В КОМАНДЕ'
      }
    }
  },
  data() {
    return {
      caption: this.label.toUpperCase(),
      statValue: this.precision ? this.precision(this.value) : this.value.toString(),
      placeInTotalRate: numberToOrdinal(this.rating, (str) => this.$t(str)),
      placeInTeamRate: this.teamRating ? numberToOrdinal(this.teamRating, (str) => this.$t(str)) : ''
    };
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .player-main-stat {
    margin: .4rem .8rem;
    align-items: center;
    text-align: center;
    width: 13rem;
    padding: .4rem 0;
  }
  .player-main-stat__value {
    font-size: 3rem;
  }
  .player-main-stat__caption {
    margin: 0 .8rem;
    font-size: 1rem;
  }
  .player-main-stat__rating {
    font-size: 2rem;
    color: @header-color;
  }
  .player-main-stat__rating-block {
    border-top: 1px solid @border-color;
    margin-top: .3rem;
    padding-top: .3rem;
  }
</style>
