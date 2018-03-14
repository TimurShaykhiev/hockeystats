import {format} from 'd3-format';
import CompUtils from 'Components/utils';

const FORMATS = [
  (d) => d.toString(),
  format('.1f'),
  format('.2f'),
  format('.3f')
];

export class NumValue {
  constructor(value, precision=2, percentage=false) {
    this.value = value;
    this.precision = FORMATS[Math.min(precision, 3)];
    this.percentage = percentage;
  }

  toStr() {
    return `${this.precision(this.value)}${this.percentage ? '%' : ''}`;
  }

  format(value) {
    return `${this.precision(value)}${this.percentage ? '%' : ''}`;
  }
}

export class TimeValue {
  constructor(value) {
    this.value = value;
  }

  toStr() {
    return CompUtils.toiToStr(this.value);
  }
}
