<template>
  <div class="bar-chart__container">
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" :height="this.height"></svg>
  </div>
</template>

<script>
import {select} from 'd3-selection';
import {scaleBand, scaleLinear} from 'd3-scale';
import {axisBottom, axisLeft} from 'd3-axis';
import {max} from 'd3-array';
import d3Tip from 'ThirdParty/d3tip';

const DEFAULT_CHART_HEIGHT = '400px';
const CHART_MARGIN = 20;

export default {
  name: 'bar-chart',
  props: {
    dataSet: {required: true},
    yCaption: {type: String},
    height: {type: String, default: DEFAULT_CHART_HEIGHT},
    tooltipFormat: {type: Function}
  },
  data() {
    return {};
  },
  mounted() {
    this.draw();
  },
  watch: {
    dataSet() {
      this.draw();
    }
  },
  methods: {
    format(value) {
      return this.tooltipFormat ? this.tooltipFormat(value) : value;
    },

    draw() {
      let svg = select(this.$el).select('svg');
      let width = svg.node().getBoundingClientRect().width - 2*CHART_MARGIN;
      let height = svg.node().getBoundingClientRect().height - 2*CHART_MARGIN;

      svg.select('g').remove();
      let g = svg.append('g')
        .attr('transform', `translate(${CHART_MARGIN},${CHART_MARGIN})`);

      let tip = d3Tip()
        .attr('class', 'bar-chart__tooltip')
        .offset([-10, 0])
        .html((d) => `<span>${this.format(d.y)}</span>`);
      svg.call(tip);

      let x = scaleBand().rangeRound([0, width]).padding(0.1);
      let y = scaleLinear().rangeRound([height, 0]);

      x.domain(this.dataSet.map((d) => d.x));
      y.domain([0, max(this.dataSet, (d) => d.y)]);

      g.append('g')
        .attr('class', 'bar-chart__axis bar-chart__axis-x')
        .attr('transform', `translate(0,${height})`)
        .call(axisBottom(x));

      g.append('g')
        .attr('class', 'bar-chart__axis bar-chart__axis-y')
        .call(axisLeft(y))
        .append('text')
          .attr('transform', 'rotate(-90)')
          .attr('y', 6)
          .attr('dy', '0.71em')
          .attr('text-anchor', 'end')
          .text(this.yCaption);

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
  .bar-chart__container {
  }
  .bar-chart__bar {
    fill: #4682B4;
    &:hover {
      fill: #A52A2A;
    }
  }
  .bar-chart__axis-x {
    path {
      display: none;
    }
  }
  .bar-chart__axis-y {
    text {
      fill: black;
    }
  }
  .bar-chart__tooltip {
    line-height: 1;
    font-weight: bold;
    padding: 12px;
    background: rgba(0, 0, 0, 0.8);
    color: #fff;
    border-radius: 2px;
    /* Creates a small triangle extender for the tooltip */
    &:after {
      box-sizing: border-box;
      display: inline;
      font-size: 10px;
      width: 100%;
      line-height: 1;
      color: rgba(0, 0, 0, 0.8);
      content: "\25BC";
      position: absolute;
      text-align: center;
    }
    /* Style northward tooltips differently */
    &.n:after {
      margin: -1px 0 0 0;
      top: 100%;
      left: 0;
    }
  }
</style>
