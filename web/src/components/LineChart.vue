<template>
  <div class="line-chart__container">
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" :height="height"></svg>
  </div>
</template>

<script>
import {select} from 'd3-selection';
import {scaleBand, scaleTime, scaleLinear} from 'd3-scale';
import {extent} from 'd3-array';
import {line, curveBasis} from 'd3-shape';
import {timeFormat} from 'd3-time-format';
import ChartUtils from 'Components/chartUtils';

export default {
  name: 'line-chart',
  props: {
    dataSet: {required: true},
    yCaption: {type: String},
    height: {type: String, default: ChartUtils.DEFAULT_CHART_HEIGHT},
    preciseYDomain: {type: Boolean, default: false},
    timeXAxis: {type: Boolean, default: false}
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
    draw() {
      this.chartData = this.dataSet;
      let svg = select(this.$el).select('svg');
      let margin = ChartUtils.getChartMargin();
      let {height, width} = ChartUtils.getBarChartSize(svg, this.chartData.length, margin);

      let x;
      if (this.timeXAxis) {
        x = scaleTime().rangeRound([0, width]);
        x.domain(extent(this.chartData, (d) => d.x));
      } else {
        x = scaleBand().rangeRound([0, width]).padding(0.1);
        x.domain(this.chartData.map((d) => d.x));
      }

      let [yMin, yMax] = extent(this.chartData, (d) => d.y);
      if (yMin > 0) {
        yMin = yMin / (this.preciseYDomain ? 1.05 : 2);
      }
      if (this.yCaption) {
        // +1 here is to expand Y axis to have extra space for caption
        ++yMax;
      }
      let y = scaleLinear().rangeRound([height, 0]);
      y.domain([yMin, yMax]).nice();

      let g = ChartUtils.prepareArea(svg, margin);

      let pathLine = line().curve(curveBasis)
        .x((d) => x(d.x))
        .y((d) => y(d.y));

      g.append('path')
        .datum(this.chartData)
        .attr('class', 'line-chart__line')
        .attr('stroke-linejoin', 'round')
        .attr('stroke-linecap', 'round')
        .attr('stroke-width', 1.5)
        .attr('d', pathLine);

      ChartUtils.prepareAxis(g, height, x, y, 'line', {
        rotateXLabels: false,
        yCaption: this.yCaption,
        disableTextWrap: this.timeXAxis,
        xTickFormat: timeFormat('%b %d')
      });
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .line-chart__line {
    fill: none;
    stroke: #4682B4;
  }
  .line-chart__axis-y {
    text {
      fill: @chart-axis-text-color;
    }
  }
  .line-chart__axis-y-caption {
    fill: @chart-axis-text-color;
    font-weight: bold;
  }
</style>
