<template>
  <div class="skaters-stats-table">
    <div v-if="showFilter" class="skaters-stats-table__filter-container container-row">
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
      styleClass="table condensed table-bordered table-striped skaters-stats-table__table">
      <template slot="table-column" slot-scope="props">
        <span :title="props.column.hint">{{props.column.label}}</span>
      </template>
      <template slot="table-row" slot-scope="props">
        <td v-for="el in columns" class="skater-stats-table__cell" v-if="!el.hidden && el.field">
          <router-link v-if="el.field === 'name'" :to="{name: 'skater', params: {id: props.row.playerId}}">
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
  name: 'skaters-stats-table',
  components: {TableFilter},
  props: {
    type: {type: String, required: true}
  },
  i18n: {
    messages: {
      en: {
        position: 'Player Position',
        positionShort: 'Pos',
        captionPlayerType: 'Carrier Statistics(since season 2013-14)',
        captionTeamType: 'Skater Statistics'
      },
      ru: {
        position: 'Амплуа игрока',
        positionShort: 'Поз',
        captionPlayerType: 'Статистика за карьеру(с сезона 2013-14)',
        captionTeamType: 'Статистика игроков'
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
        this.requestSkaterStats();
      } else {
        this.requestSkaterAllStats();
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
        return CompUtils.getSeasonName(selSeason, all, (str) => this.$t(str));
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
      return {field: 'points', type: 'desc'};
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
        label: this.$t('positionShort'),
        hint: this.$t('position'),
        field: 'position',
        sortable: this.canSortRows(),
        hidden: this.type === TYPE_PLAYER
      }, {
        label: this.$t('statNames.gamesShort'),
        hint: this.$t('statNames.games'),
        field: 'games',
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
        label: this.$t('statNames.plusMinusShort'),
        hint: this.$t('statNames.plusMinus'),
        field: 'plusMinus',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.penaltyMinutesShort'),
        hint: this.$t('statNames.penaltyMinutes'),
        field: 'penaltyMinutes',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.pointsPerGameShort'),
        hint: this.$t('statNames.pointsPerGame'),
        field: 'pointsPerGame',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.ppGoalsShort'),
        hint: this.$t('statNames.ppGoals'),
        field: 'ppGoals',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.ppPointsShort'),
        hint: this.$t('statNames.ppPoints'),
        field: 'ppPoints',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.shGoalsShort'),
        hint: this.$t('statNames.shGoals'),
        field: 'shGoals',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.shPointsShort'),
        hint: this.$t('statNames.shPoints'),
        field: 'shPoints',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.shotsShort'),
        hint: this.$t('statNames.shots'),
        field: 'shots',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.shootingPercentageShort'),
        hint: this.$t('statNames.shootingPercentage'),
        field: 'shootingPercentage',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.toiPerGameShort'),
        hint: this.$t('statNames.toiPerGame'),
        field: 'toiPerGame',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.faceOffWinsPercentageShort'),
        hint: this.$t('statNames.faceOffWinsPercentage'),
        field: 'faceOffWinsPercentage',
        type: 'number',
        sortable: this.canSortRows()
      }];
    },

    paginationText() {
      return CompUtils.getPaginationText((str) => this.$t(str));
    },

    rows() {
      let selSeason = this.$store.state.season.selectedSeason;
      let allTeams = this.$store.getters.getAllTeams(selSeason);
      if (allTeams === null && this.type !== TYPE_TEAM) {
        this.requestAllTeams();
        return [];
      }

      allTeams = allTeams.teams;
      let skaterStats;
      if (this.type === TYPE_PLAYER) {
        let stats = this.$store.getters.getSkaterAllStats(parseInt(this.$route.params.id));
        if (stats === null) {
          this.requestSkaterAllStats();
          return [];
        }
        skaterStats = stats.seasons;
      } else {
        let stats = this.type === TYPE_ALL ?
          this.$store.getters.getSkaterStats(selSeason) :
          this.$store.getters.getTeamPlayersStats(selSeason, parseInt(this.$route.params.id));
        if (stats === null) {
          if (this.type === TYPE_ALL) {
            this.requestSkaterStats();
          } else {
            this.requestTeamPlayersStats();
          }
          return [];
        }
        skaterStats = stats.skaters;
      }

      let f2 = format('.2f');
      let result = [];
      for (let t of skaterStats) {
        let rowData = Object.assign({}, t.stats);
        if (this.filterData && !this.filterData.filter(rowData)) {
          continue;
        }
        if (this.type !== TYPE_PLAYER) {
          rowData.playerId = t.player.id;
          rowData.name = t.player.name;
          rowData.position = this.$t(`playerPosition.${t.player.pos}`);
        }
        if (this.type === TYPE_ALL) {
          rowData.team = allTeams[t.player.tid].abbr;
        } else if (this.type === TYPE_PLAYER) {
          rowData.team = allTeams[t.teamId].abbr;
        }
        if (this.type === TYPE_PLAYER) {
          rowData.seasonName = CompUtils.seasonToStr(t.season, (str) => this.$t(str));
        }
        rowData.toiPerGame = CompUtils.toiToStr(rowData.toiPerGame);
        rowData.pointsPerGame = f2(rowData.pointsPerGame);
        rowData.shootingPercentage = f2(rowData.shootingPercentage);
        rowData.faceOffWinsPercentage = f2(rowData.faceOffWinsPercentage);
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

    requestSkaterStats() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getSkaterStats', {
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

    requestSkaterAllStats() {
      this.$store.dispatch('getSkaterAllStats', {playerId: this.$route.params.id});
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

  .skaters-stats-table__filter-container {
    justify-content: flex-end;
  }
  .skaters-stats-table__table {
    .desktop({
      font-size: @table-font-size-desktop;
    });
    .small-desktop({
      font-size: @table-font-size-sm-desktop;
    });
  }
  .skater-stats-table__cell {
    a {
      color: black;
      text-decoration: none;
    }
  }
</style>
