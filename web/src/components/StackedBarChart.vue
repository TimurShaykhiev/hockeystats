<template>
  <div class="stacked-bar-chart__container">
    <svg xmlns="http://www.w3.org/2000/svg" width="100%" :height="height"></svg>
    <chart-legend :names="legend" :colors="legendColors"/>
  </div>
</template>

<script>
import ChartLegend from 'Components/ChartLegend';
import {select} from 'd3-selection';
import {scaleBand, scaleLinear, scaleOrdinal, schemeCategory10} from 'd3-scale';
import {max} from 'd3-array';
import d3Tip from 'ThirdParty/d3tip';
import {DEFAULT_CHART_HEIGHT, getBarChartSize, prepareAxis, prepareArea} from 'Components/chartUtils';

export default {
  name: 'stacked-bar-chart',
  components: {ChartLegend},
  props: {
    dataSet: {required: true},
    yCaption: {type: String},
    height: {type: String, default: DEFAULT_CHART_HEIGHT},
    legend: {type: Array, required: true},
    tooltipFormat: {type: Function}
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
    format(value) {
      return this.tooltipFormat ? this.tooltipFormat(value) : value;
    },

    draw() {
      let svg = select(this.$el).select('svg');
      let {height, width} = getBarChartSize(svg, this.dataSet.length);
      let keys = this.dataSet.names;

      let x = scaleBand().rangeRound([0, width]).padding(0.1);
      let y = scaleLinear().rangeRound([height, 0]);
      let z = this.legendColors;

      let stacks = this.getStackData();

      x.domain(this.dataSet.map((d) => d.x));
      // +1 here is to expand Y axis to have extra space for caption
      y.domain([0, max(stacks, (d) => d.data.total) + 1]).nice();

      let tip = d3Tip()
        .attr('class', 'stacked-bar-chart__tooltip chart-tooltip')
        .offset([-10, 0])
        .html((d) => {
          let htmlStr = `<p>${d.data.total}</p><ul>`;
          // Iterate in reverse order to have the same order as bars in stack
          for (let i = keys.length -1; i >= 0; --i) {
            let k = keys[i];
            htmlStr += `<li><div style="background:${z(k)};"></div>${this.format(d.data[k])}</li>`;
          }
          htmlStr += '</ul>';
          return htmlStr;
        });
      svg.call(tip);

      let g = prepareArea(svg);

      g.append('g')
        .selectAll('g')
        .data(stacks)
        .enter().append('g')
          .attr('class', 'stacked-bar-chart__bar')
          .on('mouseover', tip.show)
          .on('mouseout', tip.hide)
        .selectAll('rect')
        .data((d) => d)
        .enter().append('rect')
          .attr('class', 'stacked-bar-chart__inner-bar')
          .attr('x', (d) => x(d.x))
          .attr('y', (d) => y(d[1]))
          .attr('height', (d) => y(d[0]) - y(d[1]))
          .attr('width', x.bandwidth())
          .attr('fill', (d, i) => (i === keys.length) ? '#FFF' : z(keys[i]));

      prepareAxis(g, height, x, y, 'stacked-bar', this.yCaption);
    },

    getStackData() {
      let stacks = [];
      for (let d of this.dataSet) {
        let s = [];
        let sum = 0;
        for (let k of this.dataSet.names) {
          let el = [sum, sum += d[k]];
          el.x = d.x;
          s.push(el);
        }
        // Add transparent rect which covers the whole bar for correct d3Tip work
        let el = [0, sum];
        el.x = d.x;
        s.push(el);

        s.data = d;
        s.data.total = sum;
        stacks.push(s);
      }
      return stacks;
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .stacked-bar-chart__inner-bar {
    pointer-events: none;
    &:last-of-type {
      pointer-events: all;
      opacity: 0;
    }
  }
  .stacked-bar-chart__axis-y {
    text {
      fill: @chart-axis-text-color;
    }
  }
  .stacked-bar-chart__axis-y-caption {
    fill: @chart-axis-text-color;
    font-weight: bold;
  }
  .stacked-bar-chart__tooltip {
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
