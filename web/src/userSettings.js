function isLocalStorageAvailable() {
  try {
    let storage = window['localStorage'];
    let x = '__storage_test__';
    storage.setItem(x, x);
    storage.removeItem(x);
    return true;
  } catch (e) {
    return false;
  }
}

const DEFAULT_SETTINGS = {
  locale: 'en',
  selectedSeason: {}
};

export default class UserSettings {
  constructor() {
    this._storage = isLocalStorageAvailable ? localStorage : null;
  }

  _getValue(name, parse=false) {
    let value = null;
    if (this._storage) {
      value = this._storage.getItem(name);
      if (parse && value) {
        value = JSON.parse(value);
      }
    }
    return value !== null ? value : DEFAULT_SETTINGS[name];
  }

  _setValue(name, value) {
    if (this._storage) {
      try {
        if (typeof value === 'object') {
          value = JSON.stringify(value);
        }
        this._storage.setItem(name, value);
        return true;
      } catch (e) {
        return false;
      }
    }
    return false;
  }

  get locale() {
    return this._getValue('locale');
  }

  set locale(value) {
    return this._setValue('locale', value);
  }

  get selectedSeason() {
    return this._getValue('selectedSeason', true);
  }

  set selectedSeason(value) {
    return this._setValue('selectedSeason', value);
  }
};
