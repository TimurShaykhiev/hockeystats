<template>
  <div class="team-stats-table">
    <vue-good-table
      :title="tableCaption"
      :columns="columns"
      :rows="rows"
      :paginate="false"
      :lineNumbers="showLineNumbers"
      :defaultSortBy="defaultSortColumn"
      styleClass="table condensed table-bordered table-striped team-stats-table__table">
      <template slot="table-column" slot-scope="props">
        <span :title="props.column.hint">{{props.column.label}}</span>
      </template>
      <template slot="table-row" slot-scope="props">
        <td v-for="el in columns" class="team-stats-table__cell" v-if="!el.hidden && el.field">
          <router-link v-if="el.field === 'teamName'" :to="{name: 'team', params: {id: props.row.teamId}}">
            {{props.row[el.field]}}
          </router-link>
          <span v-else>{{props.row[el.field]}}</span>
        </td>
      </template>
    </vue-good-table>
  </div>
</template>

<script>
import {SeasonRequestParams, LocaleRequestParams} from 'Store/types';
import {getSeasonName, seasonToStr} from 'Components/utils';
import {format} from 'd3-format';

const TYPE_ALL = 'all';
const TYPE_TEAM = 'team';

export default {
  name: 'teams-stats-table',
  props: {
    type: {type: String, required: true}
  },
  i18n: {
    messages: {
      en: {
        teamStatsTable: {
          caption: 'Seasons statistics'
        }
      },
      ru: {
        teamStatsTable: {
          caption: 'Статистика по сезонам'
        }
      }
    }
  },
  data() {
    return {
      showLineNumbers: this.type === TYPE_ALL
    };
  },
  created() {
    if (this.type === TYPE_ALL) {
      this.$store.dispatch('getAllTeams', {reqParams: new LocaleRequestParams(this.$store)});
      this.requestTeamStats();
    } else {
      this.requestTeamAllStats();
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
        return getSeasonName(selSeason, all, (str) => this.$t(str));
      } else {
        return this.$t('teamStatsTable.caption');
      }
    },

    defaultSortColumn() {
      if (this.type === TYPE_TEAM) {
        return {field: 'seasonName', type: 'asc'};
      }
      return {field: 'points', type: 'desc'};
    },

    columns() {
      return [{
        label: this.$t('statNames.teamShort'),
        hint: this.$t('statNames.team'),
        field: 'teamName',
        sortable: this.canSortRows(),
        hidden: this.type === TYPE_TEAM
      }, {
        label: this.$t('statNames.seasonShort'),
        hint: this.$t('statNames.season'),
        field: 'seasonName',
        sortable: this.canSortRows(),
        hidden: this.type === TYPE_ALL
      }, {
        label: this.$t('statNames.gamesShort'),
        hint: this.$t('statNames.games'),
        field: 'games',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.winRegularShort'),
        hint: this.$t('statNames.winRegular'),
        field: 'winRegular',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.winOvertimeShort'),
        hint: this.$t('statNames.winOvertime'),
        field: 'winOvertime',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.winShootoutShort'),
        hint: this.$t('statNames.winShootout'),
        field: 'winShootout',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.loseRegularShort'),
        hint: this.$t('statNames.loseRegular'),
        field: 'loseRegular',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.loseOvertimeShort'),
        hint: this.$t('statNames.loseOvertime'),
        field: 'loseOvertime',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.loseShootoutShort'),
        hint: this.$t('statNames.loseShootout'),
        field: 'loseShootout',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.pointsShort'),
        hint: this.$t('statNames.points'),
        field: 'points',
        type: 'number',
        sortable: this.canSortRows(),
        hidden: this.hidePointColumns()
      }, {
        label: this.$t('statNames.pointPercentageShort'),
        hint: this.$t('statNames.pointPercentage'),
        field: 'pointPercentage',
        type: 'number',
        sortable: this.canSortRows(),
        hidden: this.hidePointColumns()
      }, {
        label: this.$t('statNames.goalsForShort'),
        hint: this.$t('statNames.goalsFor'),
        field: 'goalsFor',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.goalsAgainstShort'),
        hint: this.$t('statNames.goalsAgainst'),
        field: 'goalsAgainst',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.goalsForPerGameShort'),
        hint: this.$t('statNames.goalsForPerGame'),
        field: 'goalsForPerGame',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.goalsAgainstPerGameShort'),
        hint: this.$t('statNames.goalsAgainstPerGame'),
        field: 'goalsAgainstPerGame',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.ppPercentageShort'),
        hint: this.$t('statNames.ppPercentage'),
        field: 'ppPercentage',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.pkPercentageShort'),
        hint: this.$t('statNames.pkPercentage'),
        field: 'pkPercentage',
        type: 'number',
        sortable: this.canSortRows()
      }, {
        label: this.$t('statNames.shotsPerGameShort'),
        hint: this.$t('statNames.shotsPerGame'),
        field: 'shotsPerGame',
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

    rows() {
      let allTeams;
      let teamStats;
      if (this.type === TYPE_ALL) {
        allTeams = this.$store.state.teams.allTeams.teams;
        if (!allTeams) {
          return [];
        }
        let selSeason = this.$store.state.season.selectedSeason;
        let stats = this.$store.getters.getTeamStats(selSeason);
        if (stats === null) {
          this.requestTeamStats();
          return [];
        }
        teamStats = stats.teams;
      } else {
        let stats = this.$store.getters.getTeamAllStats(parseInt(this.$route.params.id));
        if (stats === null) {
          this.requestTeamAllStats();
          return [];
        }
        teamStats = stats.seasons;
      }

      let f1 = format('.1f');
      let f2 = format('.2f');
      return teamStats.map((t) => {
        let rowData = Object.assign({}, t.stats);
        if (this.type === TYPE_ALL) {
          rowData.teamId = t.id;
          rowData.teamName = allTeams[t.id].name;
        } else {
          rowData.seasonName = seasonToStr(t.season, (str) => this.$t(str));
        }
        rowData.pointPercentage = f1(rowData.pointPercentage);
        rowData.goalsForPerGame = f2(rowData.goalsForPerGame);
        rowData.goalsAgainstPerGame = f2(rowData.goalsAgainstPerGame);
        rowData.ppPercentage = f1(rowData.ppPercentage);
        rowData.pkPercentage = f1(rowData.pkPercentage);
        rowData.shotsPerGame = f1(rowData.shotsPerGame);
        rowData.faceOffWinsPercentage = f1(rowData.faceOffWinsPercentage);
        return rowData;
      });
    }
  },
  methods: {
    requestTeamStats() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getTeamStats', {
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    },

    requestTeamAllStats() {
      this.$store.dispatch('getTeamAllStats', {teamId: this.$route.params.id});
    },

    hidePointColumns() {
      return this.type !== TYPE_TEAM && this.$store.state.season.selectedSeason.regular !== true;
    },

    canSortRows() {
      return this.type === TYPE_ALL;
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .team-stats-table__table {
    .desktop({
      font-size: @table-font-size-desktop;
    });
    .small-desktop({
      font-size: @table-font-size-sm-desktop;
    });
  }
  .team-stats-table__cell {
    a {
      color: black;
      text-decoration: none;
    }
  }
</style>
