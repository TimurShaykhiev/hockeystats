<template>
  <div class="games-table">
    <h2 class="games-table__caption">{{$t('gamesTable.caption')}}</h2>
    <vue-good-table
      :columns="columns"
      :rows="rows"
      :paginationOptions="{enabled: false}"
      :lineNumbers="false"
      styleClass="vgt-table condensed bordered striped stats-table__table">
      <template slot="table-column" slot-scope="props">
        <span :title="props.column.hint">{{props.column.label}}</span>
      </template>
    </vue-good-table>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import {timeFormat} from 'd3-time-format';
import {format} from 'd3-format';

const f = timeFormat('%b %e, %Y');
const f3 = format('.3f');
const WIN_TYPE_OVERTIME = 1;
const WIN_TYPE_SHOOTOUT = 2;

export default {
  name: 'games-table',
  props: {
    games: {required: true},
    team1Id: {type: Number, required: true},
    team2Id: {type: Number, required: true}
  },
  i18n: {
    messages: {
      en: {
        gamesTable: {
          caption: 'Matchups',
          overtime: ' (OT)',
          shootout: ' (SO)',
          awayHomeColumn: 'Away / Home',
          awayHomeColumnShort: 'Away / Home'
        }
      },
      ru: {
        gamesTable: {
          caption: 'Игры',
          overtime: ' (ОТ)',
          shootout: ' (Б)',
          awayHomeColumn: 'Гости / Хозяева',
          awayHomeColumnShort: 'Гости / Хозяева'
        }
      }
    }
  },
  created() {
    this.requestAllTeams();
  },
  computed: {
    columns() {
      return [{
        label: '',
        hint: '',
        field: 'gameDate',
        sortable: false
      }, {
        label: this.$t('gamesTable.awayHomeColumnShort'),
        hint: this.$t('gamesTable.awayHomeColumn'),
        field: 'score',
        sortable: false
      }, {
        label: this.$t('statNames.shotsShort'),
        hint: this.$t('statNames.shots'),
        field: 'team1Shots',
        sortable: false,
        thClass: 'compare-block--left'
      }, {
        label: this.$t('statNames.savePercentageShort'),
        hint: this.$t('statNames.savePercentage'),
        field: 'team1Svp',
        sortable: false,
        thClass: 'compare-block--left'
      }, {
        label: this.$t('statNames.powerPlayShort'),
        hint: this.$t('statNames.powerPlay'),
        field: 'team1Pp',
        sortable: false,
        thClass: 'compare-block--left'
      }, {
        label: this.$t('statNames.penaltyMinutesShort'),
        hint: this.$t('statNames.penaltyMinutes'),
        field: 'team1Pim',
        sortable: false,
        thClass: 'compare-block--left'
      }, {
        label: this.$t('statNames.shotsShort'),
        hint: this.$t('statNames.shots'),
        field: 'team2Shots',
        sortable: false,
        thClass: 'compare-block--right'
      }, {
        label: this.$t('statNames.savePercentageShort'),
        hint: this.$t('statNames.savePercentage'),
        field: 'team2Svp',
        sortable: false,
        thClass: 'compare-block--right'
      }, {
        label: this.$t('statNames.powerPlayShort'),
        hint: this.$t('statNames.powerPlay'),
        field: 'team2Pp',
        sortable: false,
        thClass: 'compare-block--right'
      }, {
        label: this.$t('statNames.penaltyMinutesShort'),
        hint: this.$t('statNames.penaltyMinutes'),
        field: 'team2Pim',
        sortable: false,
        thClass: 'compare-block--right'
      }];
    },

    rows() {
      let selSeason = this.$store.state.season.selectedSeason;
      let allTeams = this.$store.getters.getAllTeams(selSeason);
      if (allTeams === null) {
        this.requestAllTeams();
        return [];
      }

      allTeams = allTeams.teams;
      let result = [];
      for (let g of this.games) {
        let winType = '';
        if (g.winType === WIN_TYPE_OVERTIME) {
          winType = this.$t('gamesTable.overtime');
        } else if (g.winType === WIN_TYPE_SHOOTOUT) {
          winType = this.$t('gamesTable.shootout');
        }
        let rowData = {};
        rowData.gameDate = f(g.date);
        const homeName = allTeams[g.homeId].abbr;
        const awayName = allTeams[g.awayId].abbr;
        rowData.score = `${awayName}\xa0\xa0\xa0${g.awayGoals}:${g.homeGoals}${winType}\xa0\xa0\xa0${homeName}`;
        if (this.team1Id === g.homeId) {
          rowData.team1Shots = g.homeShots;
          rowData.team1Svp = f3(g.homeSvp);
          rowData.team1Pp = `${g.homePpGoals}/${g.homePpOpportunities}`;
          rowData.team1Pim = g.homePim;
          rowData.team2Shots = g.awayShots;
          rowData.team2Svp = f3(g.awaySvp);
          rowData.team2Pp = `${g.awayPpGoals}/${g.awayPpOpportunities}`;
          rowData.team2Pim = g.awayPim;
        } else {
          rowData.team1Shots = g.awayShots;
          rowData.team1Svp = f3(g.awaySvp);
          rowData.team1Pp = `${g.awayPpGoals}/${g.awayPpOpportunities}`;
          rowData.team1Pim = g.awayPim;
          rowData.team2Shots = g.homeShots;
          rowData.team2Svp = f3(g.homeSvp);
          rowData.team2Pp = `${g.homePpGoals}/${g.homePpOpportunities}`;
          rowData.team2Pim = g.homePim;
        }
        result.push(rowData);
      }
      return result;
    }
  },
  methods: {
    requestAllTeams() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getAllTeams', {
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    }
  }
};

</script>

<style lang="less">
  .games-table__caption {
    margin-bottom: 1rem;
  }
</style>
