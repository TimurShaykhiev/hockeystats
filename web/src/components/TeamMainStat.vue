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
import {floatToStr} from 'Components/utils';

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
    return {
      caption: this.label.toUpperCase(),
      statValue: floatToStr(this.value, 2),
      placeInRate: this.rating,
      leagueAverage: floatToStr(this.average, 2),
      statBarHeight: `${Math.round(this.value / Math.max(this.value, this.average) * 100)}px`,
      avgBarHeight: `${Math.round(this.average / Math.max(this.value, this.average) * 100)}px`
    };
  },
  created() {
  },
  computed: {
    statQualityClass() {
      if (this.sortOrder === 'desc') {
        return this.value > this.average ? 'good-stat' : 'bad-stat';
      }
      return this.value <= this.average ? 'good-stat' : 'bad-stat';
    }
  },
  methods: {
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .team-main-stat {
    margin: 5px 10px;
    align-items: center;
    text-align: center;
    width: 220px;
  }
  .team-main-stat__value {
    margin: 0;
    font-size: 3em;
  }
  .team-main-stat__caption {
    margin: 0 10px;
    font-size: 1em;
  }
  .team-main-stat__rating {
    margin: 0;
    font-size: 2em;
  }
  .team-main-stat__average {
    font-family: @header-font;
    font-size: 0.85em;
    width: 80px;
  }
  .team-main-stat__average-bars {
    justify-content: center;
    align-items: flex-end;
  }
  .team-main-stat__bar {
    width: 40px;
    .team-main-stat__bar-rect {
      background: darkgray;
      &.good-stat {
        background: green;
      }
      &.bad-stat {
        background: darkred;
      }
    }
  }
  .team-main-stat__avg-label {
    text-align: right;
    padding: 0 10px;
  }
  .good-stat {
    color: green;
  }
  .bad-stat {
    color: darkred;
  }
</style>
