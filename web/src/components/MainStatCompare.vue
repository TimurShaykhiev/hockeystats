<template>
  <div class="main-stat-compare container-col">
    <div class="main-stat-compare__label container-col">
      <h2>{{caption}}</h2>
    </div>
    <div class="main-stat-compare__stat-container container-row">
      <div class="main-stat-compare__stat compare--left container-col">
        <h3 class="main-stat-compare__stat-value">{{stats.left.value}}</h3>
        <h4 class="main-stat-compare__stat-rate">{{stats.left.rate}}</h4>
      </div>
      <div class="main-stat-compare__stat compare--right container-col">
        <h3 class="main-stat-compare__stat-value">{{stats.right.value}}</h3>
        <h4 class="main-stat-compare__stat-rate">{{stats.right.rate}}</h4>
      </div>
    </div>
    <div class="main-stat-compare__diff" :class="statDiff.cls">
      <h4>{{statDiff.value}}</h4>
    </div>
  </div>
</template>

<script>
import CompUtils from 'Components/utils';

export default {
  name: 'main-stat-compare',
  props: {
    label: {type: String, required: true},
    leftData: {required: true},
    rightData: {required: true},
    sortOrder: {type: String, default: 'desc'}
  },
  data() {
    return {
      caption: this.label.toUpperCase(),
      stats: {
        left: {
          value: this.leftData.value.toStr(),
          rate: CompUtils.numberToOrdinal(this.leftData.rate, (str) => this.$t(str))
        },
        right: {
          value: this.rightData.value.toStr(),
          rate: CompUtils.numberToOrdinal(this.rightData.rate, (str) => this.$t(str))
        }
      }
    };
  },
  computed: {
    statDiff() {
      let diff = this.leftData.value.value - this.rightData.value.value;
      if (diff === 0) {
        return {value: '', cls: 'diff-equal'};
      }
      let name = '';
      let cls = '';
      if (this.sortOrder === 'desc') {
        name = diff > 0 ? this.leftData.name : this.rightData.name;
        cls = diff > 0 ? 'compare-block--left' : 'compare-block--right';
        diff = Math.abs(diff);
      } else {
        name = diff < 0 ? this.leftData.name : this.rightData.name;
        cls = diff < 0 ? 'compare-block--left' : 'compare-block--right';
      }
      return {value: `${name.toUpperCase()} ${diff > 0 ? '+' : ''}${this.leftData.value.format(diff)}`, cls: cls};
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  @caption-height: 4rem;

  .main-stat-compare {
    margin: 0.4rem 0.8rem;
    justify-content: space-between;
    text-align: center;
    width: 12rem;
    height: 12rem;
    border: 1px solid @border-color;
  }
  .main-stat-compare__label {
    justify-content: center;
    width: 100%;
    height: @caption-height;
    color: #fff;
    background-color: @compare-caption-color;
    h2 {
      font-size: 1.2rem;
      padding: 0 .4rem;
    }
  }
  .main-stat-compare__stat-container {
    flex: 1;
  }
  .main-stat-compare__stat {
    flex: 1;
    justify-content: center;
    border: 1px solid @border-color;
  }
  .main-stat-compare__stat-value {
    font-size: 1.8rem;
  }
  .main-stat-compare__stat-rate {
    font-size: 1rem;
    margin-top: .5rem;
  }
  .main-stat-compare__diff {
    width: 100%;
    height: @caption-height / 2;
    &.diff-equal {
      background-color: #0f0;
    }
    h4 {
      font-size: 1.2rem;
      padding-top: .3rem;
    }
  }
</style>
