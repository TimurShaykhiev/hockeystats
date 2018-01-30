<template>
  <div class="chart-legend__container container-row">
    <div class="chart-legend__name-block" v-for="el in legend" :key="el.id">
      <div class="chart-legend__color" v-bind:style="{background: el.color}"></div>
      <span class="chart-legend__name">{{el.name}}</span>
    </div>
  </div>
</template>

<script>

export default {
  name: 'chart-legend',
  props: {
    names: {type: Array, required: true},
    colors: {required: true}
  },
  computed: {
    legend() {
      return this.names.map((name) => {
        return {id: name.key, name: name.name, color: this.colors(name.key)};
      });
    }
  }
};

</script>

<style lang="less">
  @legend-font-size: .8rem;

  .chart-legend__container {
    justify-content: flex-start;
  }
  .chart-legend__name-block {
    margin: @legend-font-size/2 @legend-font-size;
  }
  .chart-legend__color {
    position: relative;
    top: @legend-font-size / 8;
    display: inline-block;
    width: @legend-font-size;
    height: @legend-font-size;
  }
  .chart-legend__name {
    font-size: @legend-font-size;
  }
</style>
