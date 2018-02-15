import {axisBottom, axisLeft} from 'd3-axis';
import {select} from 'd3-selection';

export const DEFAULT_CHART_HEIGHT = '500px';

const CHART_MARGIN = {top: 40, bottom: 40, left: 40, right: 40};
const X_LABEL_MARGIN = 120;
const MAX_BAR_WIDTH = 80;

export function getChartMargin(rotateXLabels=false) {
  let margin = Object.assign({}, CHART_MARGIN);
  if (rotateXLabels) {
    margin.bottom += X_LABEL_MARGIN;
  }
  return margin;
}

export function getBarChartSize(svgNode, dataSetLength, margin=CHART_MARGIN) {
  let height = svgNode.node().getBoundingClientRect().height - margin.top - margin.bottom;
  let width = svgNode.node().getBoundingClientRect().width - margin.left - margin.right;
  // Reduce chart width to avoid too wide bars
  width = Math.min(width, MAX_BAR_WIDTH * (dataSetLength + 1));
  return {width: width, height: height};
}

export function prepareArea(svgNode, margin=CHART_MARGIN) {
  svgNode.select('g').remove();
  return svgNode.append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);
}

export function prepareAxis(g, height, x, y, chartName, rotateXLabels, yCaption) {
  let axisPosition = height;
  if (y.domain()[0] < 0) {
    // X axis is in the middle of the chart. Y axis contains negative values.
    axisPosition = y(0);
  }
  let axisX = g.append('g')
    .attr('class', `${chartName}-chart__axis ${chartName}-chart__axis-x`)
    .attr('transform', `translate(0,${axisPosition})`)
    .call(axisBottom(x));

  if (rotateXLabels) {
    axisX.selectAll('text')
      .call(wrapText, X_LABEL_MARGIN)
      .call(rotateLabel);
  } else {
    axisX.selectAll('text')
      .call(wrapText, x.bandwidth());
  }

  let axisY = g.append('g')
    .attr('class', `${chartName}-chart__axis ${chartName}-chart__axis-y`)
    .call(axisLeft(y));

  if (yCaption) {
    axisY.append('text')
      .attr('class', `${chartName}-chart__axis-y-caption`)
      .attr('x', 6)
      .attr('y', y(y.ticks().pop()) + 0.5)
      .attr('dy', '0.32em')
      .attr('text-anchor', 'start')
      .text(yCaption);
  }
}

function wrapText(text, width) {
  text.each((d, i, nodes) => {
    let textElem = select(nodes[i]);
    let words = textElem.text().split(/\s+/).reverse();
    let word;
    let line = [];
    let lineNumber = 0;
    let lineHeight = 1.1; // ems
    let y = textElem.attr('y');
    let dy = parseFloat(textElem.attr('dy'));
    let tspan = textElem.text(null).append('tspan')
      .attr('x', 0)
      .attr('y', y)
      .attr('dy', `${dy}em`);

    while (word = words.pop()) {
      line.push(word);
      tspan.text(line.join(' '));
      if (tspan.node().getComputedTextLength() > width) {
        line.pop();
        tspan.text(line.join(' '));
        line = [word];
        tspan = textElem.append('tspan')
          .attr('x', 0)
          .attr('y', y)
          .attr('dy', `${++lineNumber * lineHeight + dy}em`)
          .text(word);
      }
    }
  });
}

function rotateLabel(elem) {
  elem.each((d, i, nodes) => {
    let el = select(nodes[i]);
    let width = el.node().getBoundingClientRect().width;
    let height = el.node().getBoundingClientRect().height;
    el.attr('transform', `rotate(-90,0,0) translate(-${10 + width / 2},-${height})`);
  });
}
