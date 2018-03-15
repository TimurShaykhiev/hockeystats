<template>
  <div class="games-table">
    <vue-good-table
      :title="$t('gamesTable.caption')"
      :columns="columns"
      :rows="rows"
      :paginate="false"
      :lineNumbers="false"
      styleClass="table condensed table-bordered table-striped games-table__table">
      <template slot="table-column" slot-scope="props">
        <span :title="props.column.hint">{{props.column.label}}</span>
      </template>
    </vue-good-table>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import {timeFormat} from 'd3-time-format';

const f = timeFormat('%b %e %Y');
const WIN_TYPE_OVERTIME = 1;
const WIN_TYPE_SHOOTOUT = 2;

export default {
  name: 'games-table',
  props: {
    games: {required: true}
  },
  i18n: {
    messages: {
      en: {
        gamesTable: {
          caption: 'Matchups',
          overtime: 'OT',
          shootout: 'SO',
          homeColumn: 'Home',
          awayColumn: 'Away'
        }
      },
      ru: {
        gamesTable: {
          caption: 'Игры',
          overtime: 'ОТ',
          shootout: 'Б',
          homeColumn: 'Дом.',
          awayColumn: 'Гост.'
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
        field: 'gameDate'
      }, {
        label: this.$t('gamesTable.homeColumn'),
        hint: '',
        field: 'home'
      }, {
        label: '',
        hint: '',
        field: 'score'
      }, {
        label: this.$t('gamesTable.awayColumn'),
        hint: '',
        field: 'away'
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
        rowData.home = allTeams[g.homeTeamId].abbr;
        rowData.away = allTeams[g.awayTeamId].abbr;
        rowData.score = `${g.homeTeamGoals} : ${g.awayTeamGoals} ${winType}`;
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
  @import '../../styles/vars.less';

  .games-table__table {
    .desktop({
      font-size: @table-font-size-desktop;
    });
    .small-desktop({
      font-size: @table-font-size-sm-desktop;
    });
  }
</style>
