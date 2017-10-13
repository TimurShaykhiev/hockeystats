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
}
