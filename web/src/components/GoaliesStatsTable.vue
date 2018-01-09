<template>
  <div class="goalies-stats-table">
    <vue-good-table
      :title="tableCaption"
      :columns="columns"
      :rows="rows"
      :paginate="true"
      :perPage="30"
      :nextText="paginationText.next"
      :prevText="paginationText.prev"
      :rowsPerPageText="paginationText.rowsPerPage"
      :ofText="paginationText.ofText"
      :allText="paginationText.allText"
      :lineNumbers="true"
      :defaultSortBy="{field: 'wins', type: 'desc'}"
      styleClass="table condensed table-bordered table-striped goalies-stats-table__table">
      <template slot="table-column" scope="props">
        <span :title="props.column.hint">{{props.column.label}}</span>
      </template>
    </vue-good-table>
  </div>
</template>

<script>
import {SeasonRequestParams, LocaleRequestParams} from 'Store/types';
import {floatToStr, toiToStr, getSeasonName, getPaginationText} from 'Components/utils';

export default {
  name: 'goalies-stats-table',
  props: {
  },
  data() {
    return {};
  },
  created() {
    this.$store.dispatch('getAllTeams', {reqParams: new LocaleRequestParams(this.$store)});
    this.requestGoalieStats();
  },
  computed: {
    tableCaption() {
      let selSeason = this.$store.state.season.selectedSeason;
      let all = this.$store.state.season.allSeasons.seasons;
      if (selSeason.id === undefined || all === undefined) {
        return '';
      }
      return getSeasonName(selSeason, all, (str) => this.$t(str));
    },

    columns() {
      return [{
        label: '',
        hint: '',
        field: 'name',
        sortable: true,
        filterable: true,
        placeholder: ''
      }, {
        label: this.$t('statNames.teamShort'),
        hint: this.$t('statNames.team'),
        field: 'team',
        sortable: true
      }, {
        label: this.$t('statNames.gamesShort'),
        hint: this.$t('statNames.games'),
        field: 'games',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.winsShort'),
        hint: this.$t('statNames.wins'),
        field: 'wins',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.lossesShort'),
        hint: this.$t('statNames.losses'),
        field: 'losses',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.shotsAgainstShort'),
        hint: this.$t('statNames.shotsAgainst'),
        field: 'shots',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.savesShort'),
        hint: this.$t('statNames.saves'),
        field: 'saves',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.goalsAgainstShort'),
        hint: this.$t('statNames.goalsAgainst'),
        field: 'goalsAgainst',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.savePercentageShort'),
        hint: this.$t('statNames.savePercentage'),
        field: 'svp',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.goalsAgainstAverageShort'),
        hint: this.$t('statNames.goalsAgainstAverage'),
        field: 'gaa',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.timeOnIceShort'),
        hint: this.$t('statNames.timeOnIce'),
        field: 'toi',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.shutoutsShort'),
        hint: this.$t('statNames.shutouts'),
        field: 'shutout',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.goalsShort'),
        hint: this.$t('statNames.goals'),
        field: 'goals',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.assistsShort'),
        hint: this.$t('statNames.assists'),
        field: 'assists',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.pointsShort'),
        hint: this.$t('statNames.points'),
        field: 'points',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.penaltyMinutesShort'),
        hint: this.$t('statNames.penaltyMinutes'),
        field: 'penaltyMinutes',
        type: 'number',
        sortable: true
      }];
    },

    paginationText() {
      return getPaginationText((str) => this.$t(str));
    },

    rows() {
      let allTeams = this.$store.state.teams.allTeams.teams;
      if (!allTeams) {
        return [];
      }
      let selSeason = this.$store.state.season.selectedSeason;
      let stats = this.$store.state.players.goalieStats;
      let goalieStats = stats.goalies;
      if (!goalieStats || selSeason.id !== stats.season.id || selSeason.regular !== stats.season.regular) {
        this.requestGoalieStats();
        return [];
      }
      return goalieStats.map((t) => {
        let rowData = Object.assign({}, t.stats);
        rowData.name = t.player.name;
        rowData.team = allTeams[t.player.tid].abbr;
        rowData.toi = toiToStr(rowData.toi);
        rowData.gaa = floatToStr(rowData.gaa, 2);
        rowData.svp = floatToStr(rowData.svp, 3, true);
        return rowData;
      });
    }
  },
  methods: {
    requestGoalieStats() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getGoalieStats', {
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .goalies-stats-table__table {
    .desktop({
      font-size: @table-font-size-desktop;
    });
    .small-desktop({
      font-size: @table-font-size-sm-desktop;
    });
  }
</style>
