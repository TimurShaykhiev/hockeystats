<template>
  <div class="stats-block container-col">
    <div class="stats-block__caption">
      <h2>{{caption}}</h2>
    </div>
    <div class="stats-block__block container-row">
      <div v-for="el in stats" class="stats-block__item">
        <h1 class="stats-block__value">{{el.value}}</h1>
        <h3 class="stats-block__name">{{el.name}}</h3>
      </div>
    </div>
  </div>
</template>

<script>
import {floatToStr} from 'Components/utils';

export default {
  name: 'stats-block',
  props: {
    caption: {type: String, required: true},
    items: {required: true}
  },
  data() {
    return {};
  },
  computed: {
    stats() {
      return this.items.map((el) => {
        let valueStr = el.precision ? floatToStr(el.value, el.precision) : el.value.toString();
        if (el.percentage) {
          valueStr += '%';
        }
        return {name: el.name.toUpperCase(), value: valueStr};
      });
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .stats-block {
    font-family: @header-font;
    margin: 30px;
    border: dimgray 1px solid;
  }
  .stats-block__caption {
    background: darkcyan;
    height: 2.5em;
    padding-left: 20px;
  }
  .stats-block__item {
    margin: 5px;
    min-width: 10rem;
    height: 10rem;
    text-align: center;
    border-left: dimgray 1px solid;
    &:first-of-type {
      border-left: none;
    }
  }
  .stats-block__value {
    font-size: 3rem;
  }
  .stats-block__name {
    color: darkcyan;
    font-size: 1rem;
    margin: 0 0.5rem;
  }
</style>
