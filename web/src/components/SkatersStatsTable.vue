<template>
  <div class="skaters-stats-table">
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
      :defaultSortBy="{field: 'points', type: 'desc'}"
      styleClass="table condensed table-bordered table-striped skaters-stats-table__table">
      <template slot="table-column" scope="props">
        <span :title="props.column.hint">{{props.column.label}}</span>
      </template>
      <template slot="table-row" scope="props">
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
import {SeasonRequestParams, LocaleRequestParams} from 'Store/types';
import {floatToStr, toiToStr, getSeasonName, getPaginationText} from 'Components/utils';

export default {
  name: 'skaters-stats-table',
  props: {
  },
  i18n: {
    messages: {
      en: {
        position: 'Player Position',
        positionShort: 'Pos'
      },
      ru: {
        position: 'Амплуа игрока',
        positionShort: 'Поз'
      }
    }
  },
  data() {
    return {};
  },
  created() {
    this.$store.dispatch('getAllTeams', {reqParams: new LocaleRequestParams(this.$store)});
    this.requestSkaterStats();
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
        label: this.$t('positionShort'),
        hint: this.$t('position'),
        field: 'position',
        sortable: true
      }, {
        label: this.$t('statNames.gamesShort'),
        hint: this.$t('statNames.games'),
        field: 'games',
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
        label: this.$t('statNames.plusMinusShort'),
        hint: this.$t('statNames.plusMinus'),
        field: 'plusMinus',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.penaltyMinutesShort'),
        hint: this.$t('statNames.penaltyMinutes'),
        field: 'penaltyMinutes',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.pointsPerGameShort'),
        hint: this.$t('statNames.pointsPerGame'),
        field: 'pointsPerGame',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.ppGoalsShort'),
        hint: this.$t('statNames.ppGoals'),
        field: 'ppGoals',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.ppPointsShort'),
        hint: this.$t('statNames.ppPoints'),
        field: 'ppPoints',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.shGoalsShort'),
        hint: this.$t('statNames.shGoals'),
        field: 'shGoals',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.shPointsShort'),
        hint: this.$t('statNames.shPoints'),
        field: 'shPoints',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.shotsShort'),
        hint: this.$t('statNames.shots'),
        field: 'shots',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.shootingPercentageShort'),
        hint: this.$t('statNames.shootingPercentage'),
        field: 'shootingPercentage',
        type: 'number',
        sortable: true
      }, {
        label: this.$t('statNames.toiPerGameShort'),
        hint: this.$t('statNames.toiPerGame'),
        field: 'toiPerGame',
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

    paginationText() {
      return getPaginationText((str) => this.$t(str));
    },

    rows() {
      let allTeams = this.$store.state.teams.allTeams.teams;
      if (!allTeams) {
        return [];
      }
      let selSeason = this.$store.state.season.selectedSeason;
      let stats = this.$store.state.players.skaterStats;
      let skaterStats = stats.skaters;
      if (!skaterStats || selSeason.id !== stats.season.id || selSeason.regular !== stats.season.regular) {
        this.requestSkaterStats();
        return [];
      }
      return skaterStats.map((t) => {
        let rowData = Object.assign({}, t.stats);
        rowData.playerId = t.player.id;
        rowData.name = t.player.name;
        rowData.team = allTeams[t.player.tid].abbr;
        rowData.position = this.$t(`playerPosition.${t.player.pos}`);
        rowData.toiPerGame = toiToStr(rowData.toiPerGame);
        rowData.pointsPerGame = floatToStr(rowData.pointsPerGame, 2);
        rowData.shootingPercentage = floatToStr(rowData.shootingPercentage, 2);
        rowData.faceOffWinsPercentage = floatToStr(rowData.faceOffWinsPercentage, 2);
        return rowData;
      });
    }
  },
  methods: {
    requestSkaterStats() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch('getSkaterStats', {
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

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
