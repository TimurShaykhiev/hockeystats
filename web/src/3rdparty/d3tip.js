// d3.tip
// Copyright (c) 2013 Justin Palmer
// ES6 / D3 v4 Adaption Copyright (c) 2016 Constantin Gavrilete
//
// Tooltips for d3.js SVG visualizations

// Copied from https://github.com/cgav/d3-tip
// Changed for this project.

import {select as d3Select, selection as d3Selection, event as d3Event} from 'd3-selection';

export default function () {
  // Mappings to new version of d3
  const d3 = {
    select: d3Select,
    event: () => d3Event,
    selection: d3Selection,
    functor: (v) => {
      return typeof v === 'function' ? v : () => v;
    }
  };

  let direction = d3TipDirection;
  let offset = d3TipOffset;
  let html = d3TipHtml;
  let node = initNode();
  let svg = null;
  let point = null;
  let target = null;

  function tip(vis) {
    svg = getSVGNode(vis);
    point = svg.createSVGPoint();
    document.body.appendChild(node);
  }

  // Public - show the tooltip on the screen
  //
  // Returns a tip
  tip.show = function () {
    let args = Array.prototype.slice.call(arguments);
    if (args[args.length - 1] instanceof SVGElement) {
      target = args.pop();
    }

    let content = html.apply(this, args);
    let poffset = offset.apply(this, args);
    let dir = direction.apply(this, args);
    let nodel = getNodeEl();
    let i = directions.length;
    let coords;
    let scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    let scrollLeft = document.documentElement.scrollLeft || document.body.scrollLeft;

    nodel.html(content)
      .style('position', 'absolute')
      .style('opacity', 1)
      .style('pointer-events', 'all');

    while (i--) nodel.classed(directions[i], false);
    coords = directionCallbacks[dir].apply(this);
    nodel.classed(dir, true)
      .style('top', (coords.top + poffset[0]) + scrollTop + 'px')
      .style('left', (coords.left + poffset[1]) + scrollLeft + 'px');

    return tip;
  };

  // Public - hide the tooltip
  //
  // Returns a tip
  tip.hide = function () {
    let nodel = getNodeEl();
    nodel
      .style('opacity', 0)
      .style('pointer-events', 'none');
    return tip;
  };

  // Public: Proxy attr calls to the d3 tip container.  Sets or gets attribute value.
  //
  // n - name of the attribute
  // v - value of the attribute
  //
  // Returns tip or attribute value
  tip.attr = function (n, v) {
    if (arguments.length < 2 && typeof n === 'string') {
      return getNodeEl().attr(n);
    } else {
      let args = Array.prototype.slice.call(arguments);
      d3.selection.prototype.attr.apply(getNodeEl(), args);
    }

    return tip;
  };

  // Public: Proxy style calls to the d3 tip container.  Sets or gets a style value.
  //
  // n - name of the property
  // v - value of the property
  //
  // Returns tip or style property value
  tip.style = function (n, v) {
    // debugger;
    if (arguments.length < 2 && typeof n === 'string') {
      return getNodeEl().style(n);
    } else {
      let args = Array.prototype.slice.call(arguments);
      if (args.length === 1) {
        let styles = args[0];
        Object.keys(styles).forEach((key) => {
          d3.selection.prototype.style.apply(getNodeEl(), [key, styles[key]]);
        });
      }
    }

    return tip;
  };

  // Public: Set or get the direction of the tooltip
  //
  // v - One of n(north), s(south), e(east), or w(west), nw(northwest),
  //     sw(southwest), ne(northeast) or se(southeast)
  //
  // Returns tip or direction
  tip.direction = function (v) {
    if (!arguments.length) return direction;
    direction = v == null ? v : d3.functor(v);

    return tip;
  };

  // Public: Sets or gets the offset of the tip
  //
  // v - Array of [x, y] offset
  //
  // Returns offset or
  tip.offset = function (v) {
    if (!arguments.length) return offset;
    offset = v == null ? v : d3.functor(v);

    return tip;
  };

  // Public: sets or gets the html value of the tooltip
  //
  // v - String value of the tip
  //
  // Returns html value or tip
  tip.html = function (v) {
    if (!arguments.length) return html;
    html = v == null ? v : d3.functor(v);

    return tip;
  };

  // Public: destroys the tooltip and removes it from the DOM
  //
  // Returns a tip
  tip.destroy = function () {
    if (node) {
      getNodeEl().remove();
      node = null;
    }
    return tip;
  };

  function d3TipDirection() {
    return 'n';
  }

  function d3TipOffset() {
    return [0, 0];
  }

  function d3TipHtml() {
    return ' ';
  }

  let directionCallbacks = {
    n: directionN,
    s: directionS,
    e: directionE,
    w: directionW,
    nw: directionNw,
    ne: directionNe,
    sw: directionSw,
    se: directionSe
  };

  let directions = Object.keys(directionCallbacks);

  function directionN() {
    let bbox = getScreenBBox();
    return {
      top: bbox.n.y - node.offsetHeight,
      left: bbox.n.x - node.offsetWidth / 2
    };
  }

  function directionS() {
    let bbox = getScreenBBox();
    return {
      top: bbox.s.y,
      left: bbox.s.x - node.offsetWidth / 2
    };
  }

  function directionE() {
    let bbox = getScreenBBox();
    return {
      top: bbox.e.y - node.offsetHeight / 2,
      left: bbox.e.x
    };
  }

  function directionW() {
    let bbox = getScreenBBox();
    return {
      top: bbox.w.y - node.offsetHeight / 2,
      left: bbox.w.x - node.offsetWidth
    };
  }

  function directionNw() {
    let bbox = getScreenBBox();
    return {
      top: bbox.nw.y - node.offsetHeight,
      left: bbox.nw.x - node.offsetWidth
    };
  }

  function directionNe() {
    let bbox = getScreenBBox();
    return {
      top: bbox.ne.y - node.offsetHeight,
      left: bbox.ne.x
    };
  }

  function directionSw() {
    let bbox = getScreenBBox();
    return {
      top: bbox.sw.y,
      left: bbox.sw.x - node.offsetWidth
    };
  }

  function directionSe() {
    let bbox = getScreenBBox();
    return {
      top: bbox.se.y,
      left: bbox.e.x
    };
  }

  function initNode() {
    let node = d3.select(document.createElement('div'));
    node
      .style('position', 'absolute')
      .style('top', 0)
      .style('opacity', 0)
      .style('pointer-events', 'none')
      .style('box-sizing', 'border-box');

    return node.node();
  }

  function getSVGNode(el) {
    el = el.node();
    if (el.tagName.toLowerCase() === 'svg') {
      return el;
    }
    return el.ownerSVGElement;
  }

  function getNodeEl() {
    if (node === null) {
      node = initNode();
      // re-add node to DOM
      document.body.appendChild(node);
    }
    return d3.select(node);
  }

  // Private - gets the screen coordinates of a shape
  //
  // Given a shape on the screen, will return an SVGPoint for the directions
  // n(north), s(south), e(east), w(west), ne(northeast), se(southeast), nw(northwest),
  // sw(southwest).
  //
  //    +-+-+
  //    |   |
  //    +   +
  //    |   |
  //    +-+-+
  //
  // Returns an Object {n, s, e, w, nw, sw, ne, se}
  function getScreenBBox() {
    let targetel = target || d3.event().target;

    while ('undefined' === typeof targetel.getScreenCTM && 'undefined' === targetel.parentNode) {
      targetel = targetel.parentNode;
    }

    let bbox = {};
    let matrix = targetel.getScreenCTM();
    let tbbox = targetel.getBBox();
    let width = tbbox.width;
    let height = tbbox.height;
    let x = tbbox.x;
    let y = tbbox.y;

    point.x = x;
    point.y = y;
    bbox.nw = point.matrixTransform(matrix);
    point.x += width;
    bbox.ne = point.matrixTransform(matrix);
    point.y += height;
    bbox.se = point.matrixTransform(matrix);
    point.x -= width;
    bbox.sw = point.matrixTransform(matrix);
    point.y -= height / 2;
    bbox.w = point.matrixTransform(matrix);
    point.x += width;
    bbox.e = point.matrixTransform(matrix);
    point.x -= width / 2;
    point.y -= height / 2;
    bbox.n = point.matrixTransform(matrix);
    point.y += height;
    bbox.s = point.matrixTransform(matrix);

    return bbox;
  }

  return tip;
};
