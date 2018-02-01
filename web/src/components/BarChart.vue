<template>
  <div class="bar-chart__container">
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" :height="height"></svg>
  </div>
</template>

<script>
import {select} from 'd3-selection';
import {scaleBand, scaleLinear} from 'd3-scale';
import {max} from 'd3-array';
import d3Tip from 'ThirdParty/d3tip';
import {DEFAULT_CHART_HEIGHT, getBarChartSize, prepareAxis} from 'Components/chartUtils';

export default {
  name: 'bar-chart',
  props: {
    dataSet: {required: true},
    yCaption: {type: String},
    height: {type: String, default: DEFAULT_CHART_HEIGHT},
    tooltipFormat: {type: Function}
  },
  mounted() {
    this.draw();
  },
  updated() {
    this.draw();
  },
  methods: {
    format(value) {
      return this.tooltipFormat ? this.tooltipFormat(value) : value;
    },

    draw() {
      let svg = select(this.$el).select('svg');
      let {height, width} = getBarChartSize(svg, this.dataSet.length);

      let tip = d3Tip()
        .attr('class', 'chart-tooltip')
        .offset([-10, 0])
        .html((d) => `<span>${this.format(d.y)}</span>`);
      svg.call(tip);

      let x = scaleBand().rangeRound([0, width]).padding(0.1);
      let y = scaleLinear().rangeRound([height, 0]);

      x.domain(this.dataSet.map((d) => d.x));
      // +1 here is to expand Y axis to have extra space for caption
      y.domain([0, max(this.dataSet, (d) => d.y) + 1]).nice();

      let g = prepareAxis(svg, x, y, 'bar', this.yCaption);

      g.selectAll('.bar-chart__bar')
        .data(this.dataSet)
        .enter().append('rect')
          .attr('class', 'bar-chart__bar')
          .attr('x', (d) => x(d.x))
          .attr('y', (d) => y(d.y))
          .attr('width', x.bandwidth())
          .attr('height', (d) => height - y(d.y))
          .on('mouseover', tip.show)
          .on('mouseout', tip.hide);
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .bar-chart__container {
  }
  .bar-chart__bar {
    fill: #4682B4;
  }
  .bar-chart__axis-x {
    path {
      display: none;
    }
  }
  .bar-chart__axis-y {
    text {
      fill: @chart-axis-text-color;
    }
  }
  .bar-chart__axis-y-caption {
    fill: @chart-axis-text-color;
    font-weight: bold;
  }
</style>
