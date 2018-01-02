export class SeasonRequestParams {
  constructor(store, seasonId, regular) {
    this.seasonId = seasonId;
    this.seasonType = regular ? 'reg' : 'po';
    this.limit = null;
    // English locale is default, it can be omitted in request.
    this.locale = store.state.userLocale !== 'en' ? store.state.userLocale : null;
  }
  getQueryParams() {
    return [
      {name: 'sid', value: this.seasonId, required: true},
      {name: 'stype', value: this.seasonType, required: true},
      {name: 'limit', value: this.limit},
      {name: 'locale', value: this.locale}
    ];
  }
  // Returns true if requested season is the same as in storage.
  isSeasonEqual(season) {
    if (season === undefined) {
      return false;
    }
    return this.seasonId === season.seasonId && this.seasonType === season.seasonType;
  }
}

export class LocaleRequestParams {
  constructor(store) {
    // English locale is default, it can be omitted in request.
    this.locale = store.state.userLocale !== 'en' ? store.state.userLocale : null;
  }
  getQueryParams() {
    return [
      {name: 'locale', value: this.locale}
    ];
  }
}
