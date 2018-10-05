<template>
  <div class="season-stats-table">
    <vue-good-table
      :columns="columns"
      :rows="rows"
      :pagination-options="{enabled: false}"
      :lineNumbers="false"
      styleClass="vgt-table condensed bordered striped stats-table__table">
      <template slot="table-column" slot-scope="props">
        <span :title="props.column.hint">{{props.column.label}}</span>
      </template>
      <template slot="table-row" slot-scope="props">
        <div class="season-stats-table__cell">
          <span>{{props.row[props.column.field]}}</span>
        </div>
      </template>
    </vue-good-table>
  </div>
</template>

<script>
import CompUtils from 'Components/utils';
import {format} from 'd3-format';

const TYPE_REGULAR = 'regular';

export default {
  name: 'teams-stats-table',
  props: {
    type: {type: String, required: true}
  },
  created() {
    this.$store.dispatch('getSeasonStats');
  },
  computed: {
    columns() {
      return [{
        label: '',
        hint: '',
        field: 'seasonName',
        sortable: false
      }, {
        label: this.$t('statNames.gamesShort'),
        hint: this.$t('statNames.games'),
        field: 'games',
        type: 'number',
        sortable: false
      }, {
        label: this.$t('statNames.goalsForPerGameShort'),
        hint: this.$t('statNames.goalsForPerGame'),
        field: 'goalsPerGame',
        type: 'number',
        sortable: false
      }, {
        label: this.$t('statNames.shotsPerGameShort'),
        hint: this.$t('statNames.shotsPerGame'),
        field: 'shotsPerGame',
        type: 'number',
        sortable: false
      }, {
        label: this.$t('statNames.blocksPerGameShort'),
        hint: this.$t('statNames.blocksPerGame'),
        field: 'blocksPerGame',
        type: 'number',
        sortable: false
      }, {
        label: this.$t('statNames.hitsPerGameShort'),
        hint: this.$t('statNames.hitsPerGame'),
        field: 'hitsPerGame',
        type: 'number',
        sortable: false
      }, {
        label: this.$t('statNames.pimPerGameShort'),
        hint: this.$t('statNames.pimPerGame'),
        field: 'pimPerGame',
        type: 'number',
        sortable: false
      }, {
        label: this.$t('statNames.ppPercentageShort'),
        hint: this.$t('statNames.ppPercentage'),
        field: 'ppPercentage',
        type: 'number',
        sortable: false
      }, {
        label: this.$t('statNames.regularWinPercentageShort'),
        hint: this.$t('statNames.regularWinPercentage'),
        field: 'regularWinPercentage',
        type: 'number',
        sortable: false
      }, {
        label: this.$t('statNames.overtimeWinPercentageShort'),
        hint: this.$t('statNames.overtimeWinPercentage'),
        field: 'overtimeWinPercentage',
        type: 'number',
        sortable: false
      }, {
        label: this.$t('statNames.shootoutWinPercentageShort'),
        hint: this.$t('statNames.shootoutWinPercentage'),
        field: 'shootoutWinPercentage',
        type: 'number',
        sortable: false,
        hidden: this.type !== TYPE_REGULAR
      }];
    },

    rows() {
      let stats = this.$store.state.season.seasonStats;
      if (stats.regular === undefined) {
        return [];
      }
      stats = this.type === TYPE_REGULAR ? stats.regular : stats.playoff;

      let f2 = format('.2f');
      let result = [];
      for (let st of stats) {
        let rowData = {
          seasonName: CompUtils.seasonToStr(st.season),
          games: st.stats.games,
          goalsPerGame: f2(st.stats.goalsPerGame),
          shotsPerGame: f2(st.stats.shotsPerGame),
          pimPerGame: f2(st.stats.pimPerGame),
          blocksPerGame: f2(st.stats.blocksPerGame),
          hitsPerGame: f2(st.stats.hitsPerGame),
          ppPercentage: f2(st.stats.ppPercentage),
          regularWinPercentage: f2(st.stats.regularWinPercentage),
          overtimeWinPercentage: f2(st.stats.overtimeWinPercentage),
          shootoutWinPercentage: f2(st.stats.shootoutWinPercentage)
        };
        result.push(rowData);
      }
      return result;
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .stats-table__cell {
    text-align: center;
  }
</style>
