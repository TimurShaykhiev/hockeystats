<template>
  <div class="standings-table">
    <table>
      <caption>{{caption}}</caption>
      <tr>
        <th colspan="2"></th>
        <th :title="$t('statNames.games')">{{$t('statNames.gamesShort')}}</th>
        <th :title="$t('standingsHeader.wins.hint')">{{$t("standingsHeader.wins.label")}}</th>
        <th :title="$t('standingsHeader.losses.hint')">{{$t("standingsHeader.losses.label")}}</th>
        <th :title="$t('statNames.points')">{{$t("statNames.pointsShort")}}</th>
        <th :title="$t('standingsHeader.roWins.hint')">{{$t("standingsHeader.roWins.label")}}</th>
        <th :title="$t('statNames.pointPercentage')">{{$t("statNames.pointPercentageShort")}}</th>
      </tr>
      <tr v-for="elem in dataSet" :class="{'standings-table__wc': isWildCardTable}">
        <td class="rank-cell">{{elem.rank}}</td>
        <td class="name-cell">
          <router-link :to="{name: 'team', params: {id: elem.id}}">{{elem.name}}</router-link>
        </td>
        <td class="number-cell">{{elem.games}}</td>
        <td class="number-cell secondary-cell">{{elem.wins}}</td>
        <td class="number-cell secondary-cell">{{elem.losses}}</td>
        <td class="number-cell">{{elem.points}}</td>
        <td class="number-cell secondary-cell">{{elem.roWins}}</td>
        <td class="number-cell secondary-cell">{{elem.pointsPercent}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import {format} from 'd3-format';

const TYPE_CONFERENCE = 'conf';
const TYPE_DIVISION = 'div';
const TYPE_WILD_CARD = 'wc';

export default {
  name: 'standings',
  props: {
    type: {type: String, required: true},
    confSerialNum: {type: Number},
    divSerialNum: {type: Number},
    currentSeason: {type: Boolean, default: true}
  },
  i18n: {
    messages: {
      en: {
        wcTitle: 'Wild Cards',
        standingsHeader: {
          wins: {
            label: 'W',
            hint: 'Wins'
          },
          losses: {
            label: 'L',
            hint: 'Losses'
          },
          roWins: {
            label: 'ROW',
            hint: 'Regular + Overtime Wins'
          }
        }
      },
      ru: {
        wcTitle: 'Уайлд карды',
        standingsHeader: {
          wins: {
            label: 'В',
            hint: 'Победы'
          },
          losses: {
            label: 'П',
            hint: 'Поражения'
          },
          roWins: {
            label: 'ПОО',
            hint: 'Победы в основное время и в овертайме'
          }
        }
      }
    }
  },
  data() {
    return {};
  },
  created() {
    if (this.currentSeason) {
      this.$store.dispatch('getCurrentSeason').then(this.requestData);
    } else {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.requestData(season);
      }
    }
  },
  computed: {
    confId() {
      let conf = this.$store.getters.getConferenceBySerialNumber(this.confSerialNum);
      return conf !== null ? conf.id : null;
    },

    divId() {
      if (this.confId === null) {
        return null;
      }
      let divisions = [];
      let divMap = this.$store.state.teams.divisions;
      for (let k of Object.keys(divMap)) {
        if (divMap[k].cid === this.confId) {
          divisions.push(Number(k));
        }
      }
      if (divisions.length < 2) {
        return null;
      }
      // We know there can be only 2 divisions in conference
      if (this.divSerialNum === 1) {
        return Math.min(divisions[0], divisions[1]);
      }
      return Math.max(divisions[0], divisions[1]);
    },

    caption() {
      if (this.type === TYPE_CONFERENCE && this.confId !== null) {
        return this.$store.state.teams.conferences[this.confId];
      }
      if (this.type === TYPE_DIVISION && this.divId !== null) {
        return this.$store.state.teams.divisions[this.divId].name;
      }
      if (this.type === TYPE_WILD_CARD && this.divId !== null) {
        if (this.divSerialNum === undefined) {
          return this.$t('wcTitle');
        }
        return this.$store.state.teams.divisions[this.divId].name;
      }
      return '\xa0\xa0\xa0';
    },

    dataSet() {
      let season = this.currentSeason ?
        this.$store.state.season.currentSeason :
        this.$store.state.season.selectedSeason;
      if (season.id === undefined) {
        return [];
      }
      let allTeams = this.$store.getters.getAllTeams(season);
      let teamStats = this.$store.getters.getTeamStats(season);
      let standings = this.$store.getters.getStandings(season);
      if (allTeams === null || teamStats === null || standings === null) {
        this.requestData(season);
        return [];
      }
      allTeams = allTeams.teams;
      let teamsStatsMap = {};
      for (let t of teamStats.teams) {
        teamsStatsMap[t.id] = t;
      }

      if (this.type === TYPE_CONFERENCE && this.confId !== null) {
        for (let el of standings.conferences) {
          if (el.cid === this.confId) {
            standings = el.teams;
            break;
          }
        }
      } else if (this.type === TYPE_DIVISION && this.divId !== null) {
        for (let el of standings.divisions) {
          if (el.did === this.divId) {
            standings = el.teams;
            break;
          }
        }
      } else if (this.type === TYPE_WILD_CARD && this.divId !== null) {
        for (let el of standings.wildCards) {
          if (el.cid === this.confId) {
            if (this.divSerialNum === undefined) {
              standings = el.wc;
            } else {
              standings = el.div1.did === this.divId ? el.div1.teams : el.div2.teams;
            }
            break;
          }
        }
      } else {
        standings = standings.league;
      }

      let i = 0;
      let f = format('.1f');
      let result = standings.map((s) => teamsStatsMap[s]);
      return result.map((t) => {
        return {
          rank: ++i,
          id: t.id,
          name: allTeams[t.id].name,
          games: t.stats.games,
          wins: t.stats.winRegular + t.stats.winOvertime + t.stats.winShootout,
          losses: t.stats.loseRegular + t.stats.loseOvertime + t.stats.loseShootout,
          roWins: t.stats.winRegular + t.stats.winOvertime,
          points: t.stats.points,
          pointsPercent: f(t.stats.pointPercentage)
        };
      });
    },

    isWildCardTable() {
      return this.type === TYPE_WILD_CARD && this.divSerialNum === undefined;
    }
  },
  methods: {
    requestData(season) {
      let reqParams = new SeasonRequestParams(this.$store, season.id, season.regular);
      this.$store.dispatch('getAllTeams', {reqParams: reqParams});
      this.$store.dispatch('getTeamStats', {reqParams: reqParams});
      this.$store.dispatch('getTeamsStandings', {reqParams: reqParams});
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .standings-table {
    margin: .7rem;
    table {
      border-collapse: collapse;
      font-size: 1rem;
    }
    caption {
      text-align: left;
      padding-left: 1.25rem;
      color: @header-text-color;
      background: @header-color;
      line-height: 2em;
      font-size: 1.3rem;
    }
    tr {
      line-height: 1.5rem;
      border-bottom: 1px solid @border-color;
      border-collapse: collapse;
      &:last-of-type {
        border-bottom: none;
      }
    }
    tr.standings-table__wc:nth-of-type(3) {
      border-bottom: 6px solid @border-color;
    }
    th {
      border: none;
      text-align: center;
      font-weight: normal;
    }
    td {
      border: none;
      text-align: center;
      &.rank-cell {
        width: 2rem;
        background-color: #FFF;
      }
      &.number-cell {
        width: 2.5rem;
      }
      &.name-cell {
        width: 11rem;
        text-align: left;
        padding-left: .7rem;
        a {
          color: black;
          text-decoration: none;
        }
      }
      &.secondary-cell {
        color: @text-color-faded;
      }
    }
  }
</style>
