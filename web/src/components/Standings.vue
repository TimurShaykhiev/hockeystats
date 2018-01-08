<template>
  <div class="standings-table">
    <table>
      <caption>{{caption}}</caption>
      <tr>
        <th colspan="2"></th>
        <th :title="$t('statNames.games')">{{$t('statNames.gamesShort')}}</th>
        <th :title="$t('standingsHeader.wins.hint')">{{$t("standingsHeader.wins.label")}}</th>
        <th :title="$t('standingsHeader.losses.hint')">{{$t("standingsHeader.losses.label")}}</th>
        <th :title="$t('standingsHeader.lossesOT.hint')">{{$t("standingsHeader.lossesOT.label")}}</th>
        <th :title="$t('statNames.points')">{{$t("statNames.pointsShort")}}</th>
        <th :title="$t('statNames.pointPercentage')">{{$t("statNames.pointPercentageShort")}}</th>
      </tr>
      <tr v-for="elem in dataSet">
        <td class="rank-cell" :class="elem.colorMark">{{elem.rank}}</td>
        <td class="name-cell">
          <router-link :to="{name: 'team', params: {id: elem.id}}">{{elem.name}}</router-link>
        </td>
        <td class="number-cell">{{elem.games}}</td>
        <td class="number-cell secondary-cell">{{elem.wins}}</td>
        <td class="number-cell secondary-cell">{{elem.losses}}</td>
        <td class="number-cell secondary-cell">{{elem.lossesOT}}</td>
        <td class="number-cell">{{elem.points}}</td>
        <td class="number-cell secondary-cell">{{elem.pointsPercent}}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import {SeasonRequestParams, LocaleRequestParams} from 'Store/types';
import {floatToStr} from 'Components/utils';

function compareStandings(a, b) {
  // Compare points (the more the better)
  if (a.stats.points > b.stats.points) return -1;
  if (a.stats.points < b.stats.points) return 1;

  // Compare games played (the fewer the better)
  if (a.stats.games > b.stats.games) return 1;
  if (a.stats.games < b.stats.games) return -1;

  // Compare games won (the more the better). Since the 2010–11 NHL season, shootout wins are excluded from the
  // tie-breaking procedure.
  if (a.stats.winRegular + a.stats.winOvertime > b.stats.winRegular + b.stats.winOvertime) return -1;
  if (a.stats.winRegular + a.stats.winOvertime < b.stats.winRegular + b.stats.winOvertime) return 1;

  // Here we should compare the number of points earned in games between the tied clubs. I omit it for now. Team stats
  // do not have this info. Separate request is needed.

  // Compare differential between goals for and goals against (the more the better).
  if (a.stats.goalsFor - a.stats.goalsAgainst > b.stats.goalsFor - b.stats.goalsAgainst) return -1;
  if (a.stats.goalsFor - a.stats.goalsAgainst < b.stats.goalsFor - b.stats.goalsAgainst) return 1;
  return 0;
}

function getColorMarkClass(idx) {
  if (idx >= 1 && idx < 7) return 'division-top';
  if (idx === 7 || idx === 8) return 'wild-card';
  return '';
}

export default {
  name: 'standings',
  props: {
    num: {type: String, required: true}
  },
  i18n: {
    messages: {
      en: {
        standingsHeader: {
          wins: {
            label: 'W',
            hint: 'Wins(2 points)'
          },
          losses: {
            label: 'L',
            hint: 'Losses(zero points)'
          },
          lossesOT: {
            label: 'OT',
            hint: 'Overtime/shootout losses(1 point)'
          }
        }
      },
      ru: {
        standingsHeader: {
          wins: {
            label: 'В',
            hint: 'Победы(2 очка)'
          },
          losses: {
            label: 'П',
            hint: 'Поражения(0 очков)'
          },
          lossesOT: {
            label: 'ОТ',
            hint: 'Поражения в овертайме и по буллитам(1 очко)'
          }
        }
      }
    }
  },
  data() {
    return {};
  },
  created() {
    this.$store.dispatch('getAllTeams', {reqParams: new LocaleRequestParams(this.$store)});
    this.$store.dispatch('getCurrentSeason').then((season) => {
      this.$store.dispatch('getTeamStats', {
        reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
      });
    });
  },
  computed: {
    conferenceId() {
      let allTeams = this.$store.state.teams.allTeams.teams;
      let teamStats = this.$store.state.teams.teamStats.teams;
      if (!allTeams || !teamStats) {
        return '';
      }
      let conferences = [];
      for (let st of teamStats) {
        // We know there can be only 2 conferences
        if (conferences.length === 0) {
          conferences.push(allTeams[st.id].cid);
        } else if (allTeams[st.id].cid !== conferences[0]) {
          conferences.push(allTeams[st.id].cid);
          break;
        }
      }
      if (this.num === '1') {
        return Math.min(conferences[0], conferences[1]);
      }
      return Math.max(conferences[0], conferences[1]);
    },
    caption() {
      let cid = this.conferenceId;
      if (cid) {
        let conferences = this.$store.state.teams.conferences;
        for (let c of conferences) {
          if (c.id === cid) {
            return c.name;
          }
        }
      }
      return '';
    },
    dataSet() {
      let allTeams = this.$store.state.teams.allTeams.teams;
      let teamStats = this.$store.state.teams.teamStats.teams;
      let cid = this.conferenceId;
      if (!allTeams || !teamStats || !cid) {
        return [];
      }

      let confStats = teamStats.filter((el) => allTeams[el.id].cid === cid);
      let did1 = allTeams[confStats[0].id].did;
      let div1 = confStats.filter((el) => allTeams[el.id].did === did1).sort(compareStandings);
      let div2 = confStats.filter((el) => allTeams[el.id].did !== did1).sort(compareStandings);
      // Put together 3 top teams from each division and sort them
      let result = div1.slice(0, 3).concat(div2.slice(0, 3));
      result.sort(compareStandings);
      // Put together the rest teams and sort them
      let others = div1.slice(3).concat(div2.slice(3));
      others.sort(compareStandings);
      // Put sorted arrays together
      result = result.concat(others);

      let i = 0;
      return result.map((t) => {
        return {
          rank: ++i,
          colorMark: getColorMarkClass(i),
          id: t.id,
          name: allTeams[t.id].name,
          games: t.stats.games,
          wins: t.stats.winRegular + t.stats.winOvertime + t.stats.winShootout,
          losses: t.stats.loseRegular,
          lossesOT: t.stats.loseOvertime + t.stats.loseShootout,
          points: t.stats.points,
          pointsPercent: floatToStr(t.stats.pointPercentage, 1)
        };
      });
    }
  },
  methods: {
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
    }
    tr {
      border-bottom: 1px solid @border-color;
      border-collapse: collapse;
      &:last-of-type {
        border-bottom: none;
      }
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
        &.division-top {
          background-color: #008000;
        }
        &.wild-card {
          background-color: #FFA500;
        }
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
