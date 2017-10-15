const CURRENT_SEASON = 0;

export class SeasonRequestParams {
  constructor(store) {
    this.year = CURRENT_SEASON;
    this.regular = null;
    this.limit = null;
    // English locale is default, it can be omitted in request.
    this.locale = store.state.userLocale !== 'en' ? store.state.userLocale : null;
  }
  getQueryParams() {
    return [
      {name: 'year', value: this.year},
      {name: 'reg', value: this.regular},
      {name: 'limit', value: this.limit},
      {name: 'locale', value: this.locale}
    ];
  }
  // Returns true if requested season is the same as in storage.
  isSeasonEqual(season) {
    if (season === undefined) {
      return false;
    }
    if (this.year === CURRENT_SEASON && season.current === true) {
      return true;
    }
    return this.year === season.year && this.regular === season.regular;
  }
}
