import {axisBottom, axisLeft} from 'd3-axis';

export const DEFAULT_CHART_HEIGHT = '400px';
const CHART_MARGIN = 40;
const MAX_BAR_WIDTH = 80;

export function getBarChartSize(svgNode, dataSetLength) {
  let height = svgNode.node().getBoundingClientRect().height - 2*CHART_MARGIN;
  let width = svgNode.node().getBoundingClientRect().width - 2*CHART_MARGIN;
  // Reduce chart width to avoid too wide bars
  width = Math.min(width, MAX_BAR_WIDTH * (dataSetLength + 1));
  return {width: width, height: height};
}

export function prepareAxis(svgNode, x, y, chartName, yCaption) {
  let height = svgNode.node().getBoundingClientRect().height - 2*CHART_MARGIN;

  svgNode.select('g').remove();
  let g = svgNode.append('g')
    .attr('transform', `translate(${CHART_MARGIN},${CHART_MARGIN})`);

  g.append('g')
    .attr('class', `${chartName}-chart__axis ${chartName}-chart__axis-x`)
    .attr('transform', `translate(0,${height})`)
    .call(axisBottom(x));

  g.append('g')
    .attr('class', `${chartName}-chart__axis ${chartName}-chart__axis-y`)
    .call(axisLeft(y))
    .append('text')
      .attr('class', `${chartName}-chart__axis-y-caption`)
      .attr('x', 6)
      .attr('y', y(y.ticks().pop()) + 0.5)
      .attr('dy', '0.32em')
      .attr('text-anchor', 'start')
      .text(yCaption);

  return g;
}
