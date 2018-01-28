<template>
  <div class="team-main-stat container-col">
    <h1 class="team-main-stat__value" :class="statQualityClass">{{statValue}}</h1>
    <h3 class="team-main-stat__caption">{{caption}}</h3>
    <h2 class="team-main-stat__rating" :class="statQualityClass">{{placeInRate}}</h2>

    <div class="team-main-stat__average container-col">
      <div class="team-main-stat__average-bars container-row">
        <div class="team-main-stat__bar">
          <div>{{statValue}}</div>
          <div class="team-main-stat__bar-rect" :class="statQualityClass" :style="{height: statBarHeight}"></div>
        </div>
        <div class="team-main-stat__bar">
          <div>{{leagueAverage}}</div>
          <div class="team-main-stat__bar-rect" :style="{height: avgBarHeight}"></div>
        </div>
      </div>
      <div class="team-main-stat__avg-label">{{$t('average')}}</div>
    </div>
  </div>
</template>

<script>
import {numberToOrdinal} from 'Components/utils';
import {format} from 'd3-format';

export default {
  name: 'team-main-stat',
  props: {
    label: {type: String, required: true},
    value: {type: Number, required: true},
    rating: {type: Number, required: true},
    average: {type: Number, required: true},
    sortOrder: {type: String, default: 'desc'}
  },
  i18n: {
    messages: {
      en: {
        average: 'Avg'
      },
      ru: {
        average: 'Сред'
      }
    }
  },
  data() {
    let f = format('.2f');
    return {
      caption: this.label.toUpperCase(),
      statValue: f(this.value),
      placeInRate: numberToOrdinal(this.rating, (str) => this.$t(str)),
      leagueAverage: f(this.average),
      statBarHeight: `${Math.round(this.value / Math.max(this.value, this.average) * 100)}px`,
      avgBarHeight: `${Math.round(this.average / Math.max(this.value, this.average) * 100)}px`
    };
  },
  computed: {
    statQualityClass() {
      if (this.sortOrder === 'desc') {
        return this.value > this.average ? 'good-stat' : 'bad-stat';
      }
      return this.value <= this.average ? 'good-stat' : 'bad-stat';
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  @good-stat-color: #008000;
  @bad-stat-color: #8B0000;
  @bar-width: 2.5rem;

  .team-main-stat {
    margin: 0.4rem 0.8rem;
    align-items: center;
    text-align: center;
    width: 13rem;
  }
  .team-main-stat__value {
    font-size: 3rem;
    margin: 1rem 0;
  }
  .team-main-stat__caption {
    margin: 0 0.8rem;
    font-size: 1rem;
  }
  .team-main-stat__rating {
    font-size: 2rem;
    margin: 1rem 0;
  }
  .team-main-stat__average {
    font-family: @header-font;
    font-size: 0.85rem;
    width: @bar-width * 2;
  }
  .team-main-stat__average-bars {
    justify-content: center;
    align-items: flex-end;
  }
  .team-main-stat__bar {
    width: @bar-width;
    .team-main-stat__bar-rect {
      background: #A9A9A9;
      &.good-stat {
        background: @good-stat-color;
      }
      &.bad-stat {
        background: @bad-stat-color;
      }
    }
  }
  .team-main-stat__avg-label {
    text-align: right;
    padding: 0 0.8rem;
  }
  .good-stat {
    color: @good-stat-color;
  }
  .bad-stat {
    color: @bad-stat-color;
  }
</style>
