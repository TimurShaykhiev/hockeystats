<template>
  <div class="pie-chart__container">
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" :height="height"></svg>
    <chart-legend :names="legend" :colors="legendColors"/>
  </div>
</template>

<script>
import ChartLegend from 'Components/ChartLegend';
import {select} from 'd3-selection';
import {scaleOrdinal} from 'd3-scale';
import {schemePaired, schemeSet3} from 'd3-scale-chromatic';
import {pie, arc} from 'd3-shape';
import {format} from 'd3-format';
import d3Tip from 'ThirdParty/d3tip';
import ChartUtils from 'Components/chartUtils';

const MIN_ARC_WITH_TEXT_ANGLE = 0.3;
let f2 = format('.2f');

export default {
  name: 'pie-chart',
  components: {ChartLegend},
  props: {
    dataSet: {required: true},
    height: {type: String, default: ChartUtils.DEFAULT_CHART_HEIGHT},
    legend: {type: Array, required: true},
    tooltipFormat: {type: Function},
    showPercent: {type: Boolean, default: true}
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
      return scaleOrdinal(schemePaired.concat(schemeSet3)).domain(this.dataSet.map((d) => d.key));
    }
  },
  methods: {
    format(value) {
      return this.tooltipFormat ? this.tooltipFormat(value) : f2(value);
    },

    draw() {
      let svg = select(this.$el).select('svg');
      let margin = ChartUtils.getChartMargin();
      const svgRect = svg.node().getBoundingClientRect();
      let radius = (svgRect.height - margin.top - margin.bottom) / 2;
      let z = this.legendColors;

      let tip = d3Tip()
        .attr('class', 'pie-chart__tooltip chart-tooltip')
        .html((d) => {
          let val = `${this.format(d.data.value)}${this.showPercent ? '%' : ''}`;
          return `${d.data.name}: ${val}`;
        });
      svg.call(tip);

      svg.select('g').remove();
      let g = svg.append('g')
        .attr('transform', `translate(${svgRect.width / 2},${svgRect.height / 2})`);

      let pieGen = pie().value((d) => d.value);

      let path = arc().outerRadius(radius - 10).innerRadius(0);
      let label = arc().outerRadius(radius - 40).innerRadius(radius - 40);
      let circle = arc().outerRadius(radius).innerRadius(0);

      let sector = g.selectAll('.pie-chart__arc')
        .data(pieGen(this.dataSet))
        .enter().append('g')
          .attr('class', 'pie-chart__arc')
          // Pass child circle element in tip.show to display tooltip in the center of arc
          .on('mouseover', function (d, i) { tip.show(d, i, this.querySelector('circle')); })
          .on('mouseout', tip.hide);

      sector.append('path')
        .attr('d', path)
        .attr('fill', (d) => z(d.data.key));

      // If arc is too narrow - no room for text.
      sector.filter((d) => d.endAngle - d.startAngle > MIN_ARC_WITH_TEXT_ANGLE)
        .append('text')
        .attr('class', 'pie-chart__arc-label')
        .attr('transform', (d) => `translate(${label.centroid(d)})`)
        .attr('dx', '-1.5em')
        .text((d) => `${f2(d.data.value)}${this.showPercent ? '%' : ''}`);

      // Invisible circle for tooltip positioning
      sector.append('circle')
        .attr('transform', (d) => `translate(${circle.centroid(d)})`)
        .style('opacity', 0)
        .attr('r', 1);
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';
  .pie-chart__arc-label {
    font-size: .8rem;
  }
  .pie-chart__tooltip {
    p {
      margin: 0 0 .2rem 0;
      text-align: right;
    }
    ul li {
      list-style: none;
      margin: .2rem 0;
      div {
        display: inline-block;
        width: .6rem;
        height: .6rem;
        margin-right: .6rem;
      }
    }
  }
</style>
