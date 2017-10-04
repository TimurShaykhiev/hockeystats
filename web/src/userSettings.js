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
  locale: 'en'
};

export default class UserSettings {
  constructor() {
    this._storage = isLocalStorageAvailable ? localStorage : null;
  }

  _getSetting(name) {
    let value = null;
    if (this._storage) {
      value = this._storage.getItem(name);
    }
    return value !== null ? value : DEFAULT_SETTINGS[name];
  }

  _setSetting(name, value) {
    if (this._storage) {
      try {
        this._storage.setItem(name, value);
        return true;
      } catch (e) {
        return false;
      }
    }
    return false;
  }

  get locale() {
    return this._getSetting('locale');
  }

  set locale(value) {
    return this._setSetting('locale', value);
  }
};
