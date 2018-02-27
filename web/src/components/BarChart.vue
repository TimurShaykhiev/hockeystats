<template>
  <div class="bar-chart__container">
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" :height="height"></svg>
  </div>
</template>

<script>
import {select} from 'd3-selection';
import {scaleBand, scaleLinear} from 'd3-scale';
import {min, max} from 'd3-array';
import d3Tip from 'ThirdParty/d3tip';
import ChartUtils from 'Components/chartUtils';
import Utils from 'Root/utils';

export default {
  name: 'bar-chart',
  props: {
    dataSet: {required: true},
    yCaption: {type: String},
    height: {type: String, default: ChartUtils.DEFAULT_CHART_HEIGHT},
    tooltipFormat: {type: Function},
    preciseYDomain: {type: Boolean, default: false},
    sorting: {type: String},
    rotateXLabels: {type: Boolean, default: false},
    limit: {type: Number}
  },
  data() {
    return {
      chartData: this.dataSet
    };
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
      this.chartData = this.dataSet;
      let svg = select(this.$el).select('svg');
      let margin = ChartUtils.getChartMargin(this.rotateXLabels);
      let {height, width} = ChartUtils.getBarChartSize(svg, this.limit ? this.limit : this.chartData.length, margin);

      let tip = d3Tip()
        .attr('class', 'chart-tooltip')
        .offset([-10, 0])
        .html((d) => this.rotateXLabels ?
            `<span>${d.x}: ${this.format(d.y)}</span>` :
            `<span>${this.format(d.y)}</span>`);
      svg.call(tip);

      let x = scaleBand().rangeRound([0, width]).padding(0.1);
      let y = scaleLinear().rangeRound([height, 0]);

      if (this.sorting) {
        this.chartData = Utils.sortBy(this.dataSet, (e) => e.y, this.sorting === 'desc');
        if (this.limit) {
          this.chartData = this.chartData.slice(0, this.limit);
        }
      }

      x.domain(this.chartData.map((d) => d.x));

      let yMin = min(this.chartData, (d) => d.y);
      if (yMin > 0) {
        yMin = yMin / (this.preciseYDomain ? 1.05 : 2);
      }
      let yMax = max(this.chartData, (d) => d.y);
      if (this.yCaption) {
        // +1 here is to expand Y axis to have extra space for caption
        ++yMax;
      }
      y.domain([yMin, yMax]).nice();

      let g = ChartUtils.prepareArea(svg, margin);

      g.selectAll('.bar-chart__bar')
        .data(this.chartData)
        .enter().append('rect')
          .attr('class', 'bar-chart__bar')
          .attr('x', (d) => x(d.x))
          .attr('y', (d) => d.y > 0 ? y(d.y) : y(0))
          .attr('width', x.bandwidth())
          .attr('height', (d) => yMin > 0 ? height - y(d.y) : Math.abs(y(0) - y(d.y)))
          .on('mouseover', tip.show)
          .on('mouseout', tip.hide);

      ChartUtils.prepareAxis(g, height, x, y, 'bar', {
        rotateXLabels: this.rotateXLabels,
        yCaption: this.yCaption
      });
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .bar-chart__bar {
    fill: #4682B4;
    &:hover {
      fill: #3ba7b4;
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
