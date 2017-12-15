<template>
  <div class="team-stats-table">
    <vue-good-table
      :title="tableCaption"
      :columns="columns"
      :rows="rows"
      :paginate="false"
      :lineNumbers="true"
      :defaultSortBy="{field: 'points', type: 'desc'}"
      styleClass="table condensed table-bordered table-striped team-stats-table__table">
      <template slot="table-column" scope="props">
        <span :title="props.column.hint">{{props.column.label}}</span>
      </template>
    </vue-good-table>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import {floatToStr, getSeasonName} from 'Components/utils';

export default {
  name: 'teams-stats-table',
  props: {
  },
  data() {
    return {};
  },
  created() {
    this.requestTeamStats();
  },
  computed: {
    tableCaption() {
      let selSeason = this.$store.state.season.selectedSeason;
      if (selSeason.id === undefined) {
        return '';
      }
      let all = this.$store.state.season.allSeasons.seasons;
      return getSeasonName(selSeason, all, (str) => this.$t(str));
    },

    columns() {
      return [{
        label: this.$t('statNames.teamShort'),
        hint: this.$t('statNames.team'),
        field: 'teamName',
        sortable: true
      }, {
        label: this.$t('statNames.gamesShort'),
        hint: this.$t('statNames.games'),
        field: 'games',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.winRegularShort'),
        hint: this.$t('statNames.winRegular'),
        field: 'winRegular',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.winOvertimeShort'),
        hint: this.$t('statNames.winOvertime'),
        field: 'winOvertime',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.winShootoutShort'),
        hint: this.$t('statNames.winShootout'),
        field: 'winShootout',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.loseRegularShort'),
        hint: this.$t('statNames.loseRegular'),
        field: 'loseRegular',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.loseOvertimeShort'),
        hint: this.$t('statNames.loseOvertime'),
        field: 'loseOvertime',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.loseShootoutShort'),
        hint: this.$t('statNames.loseShootout'),
        field: 'loseShootout',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.pointsShort'),
        hint: this.$t('statNames.points'),
        field: 'points',
        type: 'number',
        sortable: true,
        hidden: this.$store.state.season.selectedSeason.regular !== true
      }, {
        label: this.$t('statNames.pointPercentageShort'),
        hint: this.$t('statNames.pointPercentage'),
        field: 'pointPercentage',
        type: 'number',
        sortable: true,
        hidden: this.$store.state.season.selectedSeason.regular !== true
      }, {
        label: this.$t('statNames.goalsForShort'),
        hint: this.$t('statNames.goalsFor'),
        field: 'goalsFor',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.goalsAgainstShort'),
        hint: this.$t('statNames.goalsAgainst'),
        field: 'goalsAgainst',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.goalsForPerGameShort'),
        hint: this.$t('statNames.goalsForPerGame'),
        field: 'goalsForPerGame',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.goalsAgainstPerGameShort'),
        hint: this.$t('statNames.goalsAgainstPerGame'),
        field: 'goalsAgainstPerGame',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.ppPercentageShort'),
        hint: this.$t('statNames.ppPercentage'),
        field: 'ppPercentage',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.pkPercentageShort'),
        hint: this.$t('statNames.pkPercentage'),
        field: 'pkPercentage',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.shotsPerGameShort'),
        hint: this.$t('statNames.shotsPerGame'),
        field: 'shotsPerGame',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.faceOffWinsPercentageShort'),
        hint: this.$t('statNames.faceOffWinsPercentage'),
        field: 'faceOffWinsPercentage',
        type: 'number',
        sortable: true
      }];
    },

    rows() {
      let selSeason = this.$store.state.season.selectedSeason;
      let stats = this.$store.state.teams.teamStats;
      let teamStats = stats.teams;
      if (!teamStats || selSeason.id !== stats.season.id || selSeason.regular !== stats.season.regular) {
        this.requestTeamStats();
        return [];
      }
      return teamStats.map((t) => {
        let rowData = Object.assign({}, t.stats);
        rowData.teamName = this.$t(`teams.${t.team.id}`);
        rowData.pointPercentage = floatToStr(rowData.pointPercentage, 1);
        rowData.goalsForPerGame = floatToStr(rowData.goalsForPerGame, 2);
        rowData.goalsAgainstPerGame = floatToStr(rowData.goalsAgainstPerGame, 2);
        rowData.ppPercentage = floatToStr(rowData.ppPercentage, 1);
        rowData.pkPercentage = floatToStr(rowData.pkPercentage, 1);
        rowData.shotsPerGame = floatToStr(rowData.shotsPerGame, 1);
        rowData.faceOffWinsPercentage = floatToStr(rowData.faceOffWinsPercentage, 1);
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
        return true;
      }
      return false;
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
</style>
