<template>
  <div class="line-chart__container">
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" :height="height"></svg>
    <chart-legend v-if="legend" :names="legend" :colors="legendColors"/>
  </div>
</template>

<script>
import {select} from 'd3-selection';
import {scaleLinear, scaleOrdinal} from 'd3-scale';
import {schemeCategory10} from 'd3-scale-chromatic';
import {extent, merge} from 'd3-array';
import {line, curveBasis} from 'd3-shape';
import {timeFormat} from 'd3-time-format';
import ChartUtils from 'Components/chartUtils';
import ChartLegend from 'Components/ChartLegend';

export default {
  name: 'line-chart',
  components: {ChartLegend},
  props: {
    dataSet: {required: true},
    yCaption: {type: String},
    height: {type: String, default: ChartUtils.DEFAULT_CHART_HEIGHT},
    preciseYDomain: {type: Boolean, default: false},
    legend: {type: Array}
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
  computed: {
    legendColors() {
      return scaleOrdinal(schemeCategory10).domain(this.dataSet.names);
    }
  },
  methods: {
    draw() {
      this.chartData = this.dataSet;
      let svg = select(this.$el).select('svg');
      let margin = ChartUtils.getChartMargin();
      let {height, width} = ChartUtils.getBarChartSize(svg, this.chartData.data[0].length, margin);
      let keys = this.dataSet.names;

      let x = scaleLinear().rangeRound([0, width]);
      x.domain(this.getAxisMinMax((d) => d.x));

      let [yMin, yMax] = this.getAxisMinMax((d) => d.y);
      if (yMin > 0) {
        yMin = yMin / (this.preciseYDomain ? 1.05 : 2);
      }
      if (this.yCaption) {
        // +1 here is to expand Y axis to have extra space for caption
        ++yMax;
      }
      let y = scaleLinear().rangeRound([height, 0]);
      y.domain([yMin, yMax]).nice();
      let z = this.legendColors;

      let g = ChartUtils.prepareArea(svg, margin);

      let pathLine = line().curve(curveBasis)
        .x((d) => x(d.x))
        .y((d) => y(d.y));

      let lines = g.selectAll('line-chart__line-container')
        .data(this.chartData.data)
        .enter().append('g')
          .attr('class', 'line-chart__line-container');

      lines.append('path')
        .attr('class', 'line-chart__line')
        .attr('stroke-linejoin', 'round')
        .attr('stroke-linecap', 'round')
        .attr('stroke-width', 1.5)
        .attr('stroke', (d, i) => z(keys[i]))
        .attr('d', pathLine);

      ChartUtils.prepareAxis(g, height, x, y, 'line', {
        rotateXLabels: false,
        yCaption: this.yCaption,
        disableTextWrap: true,
        xTickFormat: timeFormat('%b %d')
      });
    },

    getAxisMinMax(accessor) {
      return extent(merge(this.chartData.data.map((d) => extent(d, accessor))));
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .line-chart__line {
    fill: none;
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
