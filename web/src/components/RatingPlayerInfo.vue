<template>
  <div class="rating-player-info container-col">
    <span class="ratings__player-name">{{name}}</span>
    <span class="ratings__team-name">{{team}}</span>
    <div v-if="showValueBar" class="rating-player-info__value-bar container-row">
      <span v-if="this.sharedValueBarRight" class="rating-player-info__value">{{valueStr}}</span>
      <div class="rating-player-info__bar-rect-container  container-row">
        <div class="rating-player-info__bar-rect" :class="bar1Class" :style="{width: bar1Width}"></div>
        <div class="rating-player-info__bar-rect" :class="bar2Class" :style="{width: bar2Width}"></div>
      </div>
      <span v-if="!this.sharedValueBarRight" class="rating-player-info__value">{{valueStr}}</span>
    </div>
  </div>
</template>

<script>

export default {
  name: 'rating-player-info',
  props: {
    name: {type: String, required: true},
    team: {type: String, required: true},
    value: {type: Number},
    sharedValue: {type: Number},
    showValueBar: {type: Boolean, default: false},
    sharedValueBarRight: {type: Boolean, default: false},
    valueFormat: {type: Function}
  },
  data() {
    let cls1 = '';
    let cls2 = '';
    let w1 = 0;
    let w2 = 0;
    if (this.showValueBar) {
      if (this.sharedValue === undefined) {
        cls1 = 'rating-player-info__main-bar';
        w1 = 100;
      } else {
        cls1 = this.sharedValueBarRight ? 'rating-player-info__main-bar' : 'rating-player-info__secondary-bar';
        cls2 = this.sharedValueBarRight ? 'rating-player-info__secondary-bar' : 'rating-player-info__main-bar';
        const sharedValuePercent = Math.round(this.sharedValue / this.value * 100);
        w1 = this.sharedValueBarRight ? 100 - sharedValuePercent : sharedValuePercent;
        w2 = this.sharedValueBarRight ? sharedValuePercent : 100 - sharedValuePercent;
      }
    }
    return {
      valueStr: this.valueFormat ? this.valueFormat(this.value) : this.value,
      bar1Class: cls1,
      bar2Class: cls2,
      bar1Width: `${w1}%`,
      bar2Width: `${w2}%`
    };
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  @value-color: #008000;
  @shared-value-color: #eabf29;
  @bar-height: 1.5rem;

  .ratings__player-name {
    display: block;
    font-size: 1.3rem;
  }
  .ratings__team-name {
    display: block;
    font-size: .9rem;
  }
  .rating-player-info__value-bar {
    justify-content: center;
    margin-top: .5rem;
  }
  .rating-player-info__value {
    display: block;
    flex: 1;
    font-family: @header-font;
    font-size: 1rem;
  }
  .rating-player-info__bar-rect-container {
    flex: 10;
  }
  .rating-player-info__bar-rect {
    height: @bar-height;
    &.rating-player-info__main-bar {
      background: @value-color;
    }
    &.rating-player-info__secondary-bar {
      background: @shared-value-color;
    }
  }
</style>
