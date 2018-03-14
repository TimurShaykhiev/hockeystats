<template>
  <div class="goalies-stats-table">
    <div v-if="showFilter" class="goalies-stats-table__filter-container container-row">
      <table-filter :columns="columns" v-on:apply-table-filter="applyFilter" v-on:reset-table-filter="resetFilter"/>
    </div>
    <vue-good-table
      :title="tableCaption"
      :columns="columns"
      :rows="rows"
      :paginate="showPagination"
      :perPage="30"
      :nextText="paginationText.next"
      :prevText="paginationText.prev"
      :rowsPerPageText="paginationText.rowsPerPage"
      :ofText="paginationText.ofText"
      :allText="paginationText.allText"
      :lineNumbers="showLineNumbers"
      :defaultSortBy="defaultSortColumn"
      styleClass="table condensed table-bordered table-striped goalies-stats-table__table">
      <template slot="table-column" slot-scope="props">
        <span :title="props.column.hint">{{props.column.label}}</span>
      </template>
      <template slot="table-row" slot-scope="props">
        <td v-for="el in columns" class="goalie-stats-table__cell" v-if="!el.hidden && el.field">
          <router-link v-if="el.field === 'name'" :to="{name: 'goalie', params: {id: props.row.playerId}}">
            {{props.row[el.field]}}
          </router-link>
          <span v-else>{{props.row[el.field]}}</span>
        </td>
      </template>
    </vue-good-table>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import CompUtils from 'Components/utils';
import TableFilter from 'Components/TableFilter';
import {format} from 'd3-format';

const TYPE_ALL = 'all';
const TYPE_TEAM = 'team';
const TYPE_PLAYER = 'player';

export default {
  name: 'goalies-stats-table',
  components: {TableFilter},
  props: {
    type: {type: String, required: true}
  },
  i18n: {
    messages: {
      en: {
        captionPlayerType: 'Carrier Statistics(since season 2013-14)',
        captionTeamType: 'Goaltender Statistics'
      },
      ru: {
        captionPlayerType: 'Статистика за карьеру(с сезона 2013-14)',
        captionTeamType: 'Статистика вратарей'
      }
    }
  },
  data() {
    return {
      showLineNumbers: this.type !== TYPE_PLAYER,
      showPagination: this.type === TYPE_ALL,
      showFilter: this.type === TYPE_ALL,
      filterData: null
    };
  },
  created() {
    if (this.type === TYPE_TEAM) {
      this.requestTeamPlayersStats();
    } else {
      this.requestAllTeams();
      if (this.type === TYPE_ALL) {
        this.requestGoalieStats();
      } else {
        this.requestGoalieAllStats();
      }
    }
  },
  computed: {
    tableCaption() {
      if (this.type === TYPE_ALL) {
        let selSeason = this.$store.state.season.selectedSeason;
        let all = this.$store.state.season.allSeasons.seasons;
        if (selSeason.id === undefined || all === undefined) {
          return '';
        }
        return CompUtils.getSeasonName(selSeason, all);
      } else if (this.type === TYPE_TEAM) {
        return this.$t('captionTeamType');
      } else {
        return this.$t('captionPlayerType');
      }
    },

    defaultSortColumn() {
      if (this.type === TYPE_PLAYER) {
        return {field: 'seasonName', type: 'asc'};
      }
      return {field: 'wins', type: 'desc'};
    },

    columns() {
      return [{
        label: '',
        hint: '',
        field: 'name',
        sortable: this.canSortRows(),
        filterable: this.type === TYPE_ALL,
        filter: CompUtils.filterName,
        placeholder: '',
        hidden: this.type === TYPE_PLAYER
      }, {
        label: this.$t('statNames.seasonShort'),
        hint: this.$t('statNames.season'),
        field: 'seasonName',
        sortable: this.canSortRows(),
        hidden: this.type !== TYPE_PLAYER
      }, {
        label: this.$t('statNames.teamShort'),
        hint: this.$t('statNames.team'),
        field: 'team',
        sortable: this.canSortRows(),
        hidden: this.type === TYPE_TEAM
      }, {
        label: this.$t('statNames.gamesShort'),
        hint: this.$t('statNames.games'),
        field: 'games',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.winsShort'),
        hint: this.$t('statNames.wins'),
        field: 'wins',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.lossesShort'),
        hint: this.$t('statNames.losses'),
        field: 'losses',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.shotsAgainstShort'),
        hint: this.$t('statNames.shotsAgainst'),
        field: 'shots',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.savesShort'),
        hint: this.$t('statNames.saves'),
        field: 'saves',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.goalsAgainstShort'),
        hint: this.$t('statNames.goalsAgainst'),
        field: 'goalsAgainst',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.savePercentageShort'),
        hint: this.$t('statNames.savePercentage'),
        field: 'svp',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.goalsAgainstAverageShort'),
        hint: this.$t('statNames.goalsAgainstAverage'),
        field: 'gaa',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.timeOnIceShort'),
        hint: this.$t('statNames.timeOnIce'),
        field: 'toi',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.shutoutsShort'),
        hint: this.$t('statNames.shutouts'),
        field: 'shutout',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.goalsShort'),
        hint: this.$t('statNames.goals'),
        field: 'goals',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.assistsShort'),
        hint: this.$t('statNames.assists'),
        field: 'assists',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.pointsShort'),
        hint: this.$t('statNames.points'),
        field: 'points',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.penaltyMinutesShort'),
        hint: this.$t('statNames.penaltyMinutes'),
        field: 'penaltyMinutes',
        type: 'number',
        sortable: this.canSortRows()
      }];
    },

    paginationText() {
      return CompUtils.getPaginationText();
    },

    rows() {
      let selSeason = this.$store.state.season.selectedSeason;
      let allTeams = this.$store.getters.getAllTeams(selSeason);
      if (allTeams === null && this.type !== TYPE_TEAM) {
        this.requestAllTeams();
        return [];
      }

      allTeams = allTeams.teams;
      let goalieStats;
      if (this.type === TYPE_PLAYER) {
        let stats = this.$store.getters.getGoalieAllStats(parseInt(this.$route.params.id));
        if (stats === null) {
          this.requestGoalieAllStats();
          return [];
        }
        goalieStats = stats.seasons;
      } else {
        let stats = this.type === TYPE_ALL ?
          this.$store.getters.getGoalieStats(selSeason) :
          this.$store.getters.getTeamPlayersStats(selSeason, parseInt(this.$route.params.id));
        if (stats === null) {
          if (this.type === TYPE_ALL) {
            this.requestGoalieStats();
          } else {
            this.requestTeamPlayersStats();
          }
          return [];
        }
        goalieStats = stats.goalies;
      }

      let f2 = format('.2f');
      let result = [];
      for (let t of goalieStats) {
        let rowData = Object.assign({}, t.stats);
        if (this.filterData && !this.filterData.filter(rowData)) {
          continue;
        }
        if (this.type !== TYPE_PLAYER) {
          rowData.playerId = t.player.id;
          rowData.name = t.player.name;
        }
        if (this.type === TYPE_ALL) {
          rowData.team = allTeams[t.player.tid].abbr;
        } else if (this.type === TYPE_PLAYER) {
          rowData.team = allTeams[t.teamId].abbr;
        }
        if (this.type === TYPE_PLAYER) {
          rowData.seasonName = CompUtils.seasonToStr(t.season);
        }
        rowData.toi = CompUtils.toiToStr(rowData.toi);
        rowData.gaa = f2(rowData.gaa);
        rowData.svp = CompUtils.omitInteger(rowData.svp, 3);
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
    },

    requestGoalieStats() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getGoalieStats', {
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    },

    requestTeamPlayersStats() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getTeamPlayersStats', {
          teamId: this.$route.params.id,
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    },

    requestGoalieAllStats() {
      this.$store.dispatch('getGoalieAllStats', {playerId: this.$route.params.id});
    },

    canSortRows() {
      return this.type !== TYPE_PLAYER;
    },

    applyFilter(filterData) {
      if (!filterData.isEqual(this.filterData)) {
        this.filterData = filterData;
      }
    },

    resetFilter() {
      this.filterData = null;
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .goalies-stats-table__filter-container {
    justify-content: flex-end;
  }
  .goalies-stats-table__table {
    .desktop({
      font-size: @table-font-size-desktop;
    });
    .small-desktop({
      font-size: @table-font-size-sm-desktop;
    });
  }
  .goalie-stats-table__cell {
    a {
      color: black;
      text-decoration: none;
    }
  }
</style>
