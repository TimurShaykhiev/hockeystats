import {format} from 'd3-format';
import CompUtils from 'Components/utils';
import i18n from 'Root/locales';

const FORMATS = [
  (d) => d.toString(),
  format('.1f'),
  format('.2f'),
  format('.3f')
];

export class NumValue {
  constructor(value, precision=2) {
    this.value = value;
    this.precision = FORMATS[Math.min(precision, 3)];
  }

  toStr() {
    return this.precision(this.value);
  }

  toOrdinal() {
    // Now it is applicable for english and russian languages only
    const rem = this.value % 100;
    if (rem === 11 || rem === 12) {
      return `${this.value}${i18n.t('ordinalNumbers[0]')}`;
    }
    return `${this.value}${i18n.t(`ordinalNumbers[${this.value % 10}]`)}`;
  }

  format(value) {
    return this.precision(value);
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
