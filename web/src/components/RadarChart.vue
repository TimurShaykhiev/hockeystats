<template>
  <div class="radar-chart__container">
    <svg xmlns="http://www.w3.org/2000/svg" :width="height" :height="height"></svg>
    <chart-legend v-if="legend" :names="legend" :colors="colors"/>
  </div>
</template>

<script>
// This component is based on source code from http://bl.ocks.org/nbremer/6506614,
// which is based on https://github.com/alangrafu/radar-chart-d3

import ChartLegend from 'Components/ChartLegend';
import {select} from 'd3-selection';
import {scaleLinear, scaleOrdinal, schemeCategory10} from 'd3-scale';
import {max} from 'd3-array';
import {CHART_MARGIN} from 'Components/chartUtils';

const DEFAULT_RADAR_CHART_HEIGHT = '600px';

export default {
  name: 'radar-chart',
  components: {ChartLegend},
  props: {
    dataSet: {required: true},
    axises: {required: true},
    homogeneous: {type: Boolean, default: true},
    height: {type: String, default: DEFAULT_RADAR_CHART_HEIGHT},
    legend: {type: Array}
  },
  data() {
    return {
      chartRadius: 0,
      nodeRadius: 5,
      factor: 1,
      factorLegend: .85,
      levels: 5,
      sector: 2 * Math.PI / this.axises.length,
      opacityArea: 0.5,
      ToRight: 5,
      colors: scaleOrdinal(schemeCategory10).domain(this.dataSet.map((d) => d.legendKey))
    };
  },
  mounted() {
    this.draw();
  },
  updated() {
    this.draw();
  },
  methods: {
    draw() {
      let svg = select(this.$el).select('svg');
      this.chartRadius = (svg.node().getBoundingClientRect().height - 2*CHART_MARGIN) / 2;

      svg.select('g').remove();
      let g = svg.append('g')
        .attr('transform', `translate(${CHART_MARGIN},${CHART_MARGIN})`);

      if (this.homogeneous) {
        this.addAxisScales();
        this.drawLevels(g);
        this.drawSimpleAxis(g);
      }

      // Draw polygons
      this.dataSet.forEach((areaData) => {
        let areaId = areaData.legendKey;
        let polygonNodes = [];
        g.selectAll('.radar-chart__node')
          .data(areaData.data, (d, i) => {
            let value = this.getAxisValue(d, i);
            polygonNodes.push([
              this.getXCoord(this.chartRadius, i, value),
              this.getYCoord(this.chartRadius, i, value)
            ]);
          });
        polygonNodes.push(polygonNodes[0]);

        g.selectAll('.area')
          .data([polygonNodes])
          .enter()
          .append('polygon')
            .attr('class', `radar-chart__polygon radar-chart__area${areaId}`)
            .style('stroke', this.colors(areaId))
            .attr('points', (d) => d.map((p) => p.join(',')).join(' '))
            .style('fill', () => this.colors(areaId))
            .style('fill-opacity', this.opacityArea)
            .on('mouseover', (d, i, nodes) => {
              g.selectAll('polygon')
                .style('fill-opacity', 0.1);
              select(nodes[i])
                .style('fill-opacity', .7);
            })
            .on('mouseout', () => {
              g.selectAll('polygon')
                .style('fill-opacity', this.opacityArea);
            });
      });

      // Draw points on axis
      this.dataSet.forEach((areaData) => {
        let areaId = areaData.legendKey;
        g.selectAll('.radar-chart__node')
          .data(areaData.data).enter()
          .append('svg:circle')
            .attr('class', `radar-chart__axis-point radar-chart__area${areaId}`)
            .attr('r', this.nodeRadius)
            .attr('alt', (d) => Math.max(d.value, 0))
            .attr('cx', (d, i) => this.getXCoord(this.chartRadius, i, this.getAxisValue(d, i)))
            .attr('cy', (d, i) => this.getYCoord(this.chartRadius, i, this.getAxisValue(d, i)))
            .attr('data-id', (d) => d.key)
            .style('fill', this.colors(areaId))
            .append('svg:title')
              .text((j) => Math.max(j.value, 0));
      });
    },

    drawLevels(g) {
      let radius = this.factor * Math.min(this.chartRadius, this.chartRadius);

      // Circular segments
      for (let j = 0; j < this.levels - 1; j++) {
        let levelFactor = this.factor * radius * ((j + 1) / this.levels);
        g.selectAll('.levels')
          .data(this.axises)
          .enter()
          .append('svg:line')
          .attr('x1', (d, i) => this.getXCoord(levelFactor, i))
          .attr('y1', (d, i) => this.getYCoord(levelFactor, i))
          .attr('x2', (d, i) => this.getXCoord(levelFactor, i + 1))
          .attr('y2', (d, i) => this.getYCoord(levelFactor, i + 1))
          .attr('class', 'radar-chart__level')
          .attr('transform', `translate(${(this.chartRadius - levelFactor)},${(this.chartRadius - levelFactor)})`);
      }

      // Level text
      let levelScale = this.axises[0].axisScale.range([0, radius]).ticks(this.levels + 1);
      for (let j = 0; j < this.levels; j++) {
        let levelFactor = this.factor * radius * ((j + 1) / this.levels);
        g.selectAll('.levels')
          .data([1]) // dummy data
          .enter()
          .append('svg:text')
            .attr('x', levelFactor)
            .attr('y', levelFactor * (1 - this.factor))
            .attr('class', 'radar-chart__scale')
            .attr('transform',
              `translate(${(this.chartRadius - levelFactor + this.ToRight)},${(this.chartRadius - levelFactor)})`)
            .text(levelScale[j+1]);
        }
    },

    drawSimpleAxis(g) {
      let axis = g.selectAll('.radar-chart__axis')
        .data(this.axises)
        .enter()
        .append('g')
        .attr('class', 'radar-chart__axis');

      axis.append('line')
        .attr('x1', this.chartRadius)
        .attr('y1', this.chartRadius)
        .attr('x2', (d, i) => this.getXCoord(this.chartRadius, i))
        .attr('y2', (d, i) => this.getYCoord(this.chartRadius, i))
        .attr('class', 'radar-chart__axis-line');

      axis.append('text')
        .attr('class', 'radar-chart__axis-name')
        .text((d) => d.name)
        .attr('text-anchor', 'middle')
        .attr('dy', '1.5em')
        .attr('transform', 'translate(0, -10)')
        .attr('x', (d, i) => {
          return this.chartRadius *
            (1 - this.factorLegend * Math.sin(i * this.sector)) - 60 * Math.sin(i * this.sector);
        })
        .attr('y', (d, i) => {
          return this.chartRadius * (1 - Math.cos(i * this.sector)) - 20 * Math.cos(i * this.sector);
        });
    },

    getXCoord(radius, i, value=1) {
      return radius * (1 - value * this.factor * Math.sin(i * this.sector));
    },

    getYCoord(radius, i, value=1) {
      return radius * (1 - value * this.factor * Math.cos(i * this.sector));
    },

    addAxisScales() {
      // If axises are homogeneous(contain values of the same type), calculate common range for all axises
      let totalMax = max(this.dataSet, (i) => max(i.data.map((o) => o.value)));
      let axisScale = this.getAxisScale([0, totalMax]);
      for (let a of this.axises) {
        a.axisScale = axisScale;
      }
    },

    getAxisScale(range) {
      return scaleLinear().domain(range).nice(this.levels + 1);
    },

    getAxisValue(data, i) {
      // We get max domain value from axisScale
      return Math.max(data.value, 0) / this.axises[i].axisScale.domain()[1];
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  @axis-line-color: #808080;

  .radar-chart__container {
  }
  .radar-chart__level {
    stroke: @axis-line-color;
    stroke-opacity: .75;
    stroke-width: .3px;
  }
  .radar-chart__scale {
    font-size: 10px;
    fill: @chart-axis-text-color;
  }
  .radar-chart__axis-line {
    stroke: @axis-line-color;
    stroke-width: 1px;
  }
  .radar-chart__axis-name {
    font-size: 11px;
    fill: @chart-axis-text-color;
  }
  .radar-chart__polygon {
    stroke-width: 2px;
  }
  .radar-chart__axis-point {
    fill-opacity: .9;
  }
</style>
