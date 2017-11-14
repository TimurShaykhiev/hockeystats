<template>
  <div class="standings-table">
    <table>
      <caption>{{caption}}</caption>
      <tr>
        <th colspan="2"></th>
        <th :title="$t('standingsHeader.gamesPlayed.hint')">{{$t('standingsHeader.gamesPlayed.label')}}</th>
        <th :title="$t('standingsHeader.wins.hint')">{{$t("standingsHeader.wins.label")}}</th>
        <th :title="$t('standingsHeader.losses.hint')">{{$t("standingsHeader.losses.label")}}</th>
        <th :title="$t('standingsHeader.lossesOT.hint')">{{$t("standingsHeader.lossesOT.label")}}</th>
        <th :title="$t('standingsHeader.points.hint')">{{$t("standingsHeader.points.label")}}</th>
        <th :title="$t('standingsHeader.pointsPercent.hint')">{{$t("standingsHeader.pointsPercent.label")}}</th>
      </tr>
      <tr v-for="elem in dataSet">
        <td class="rank-cell" :class="elem.colorMark">{{elem.rank}}</td>
        <td class="name-cell">{{elem.name}}</td>
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
import {SeasonRequestParams} from 'Store/types';

function getPointsPercentStr(points, games) {
  let pp = 0;
  if (games > 0) {
    pp = points * 100 / (games * 2);
  }
  return `${Math.floor(pp)}%`;
}

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
          gamesPlayed: {
            label: 'GP',
            hint: 'Games played'
          },
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
          },
          points: {
            label: 'P',
            hint: 'Points'
          },
          pointsPercent: {
            label: '%P',
            hint: '% points'
          }
        }
      },
      ru: {
        standingsHeader: {
          gamesPlayed: {
            label: 'И',
            hint: 'Игры'
          },
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
          },
          points: {
            label: 'О',
            hint: 'Очки'
          },
          pointsPercent: {
            label: '%О',
            hint: 'Процент набранных очков'
          }
        }
      }
    }
  },
  data() {
    return {};
  },
  created() {
    this.$store.dispatch('getCurrentSeason').then((season) => {
      this.$store.dispatch('getTeamStats', {
        reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
      });
    });
  },
  computed: {
    conferenceId() {
      let conferences = this.$store.state.teams.conferences;
      if (conferences.length === 0) {
        return '';
      }
      if (this.num === '1') {
        return Math.min(conferences[0].id, conferences[1].id);
      }
      return Math.max(conferences[0].id, conferences[1].id);
    },
    caption() {
      let cid = this.conferenceId;
      if (cid) {
        return this.$t(`conferences.${cid}`);
      }
      return '';
    },
    dataSet() {
      let teamStats = this.$store.state.teams.teamStats.teams;
      let cid = this.conferenceId;
      if (!teamStats || !cid) {
        return [];
      }

      let confStats = teamStats.filter((el) => el.team.cid === cid);
      let did1 = confStats[0].team.did;
      let div1 = confStats.filter((el) => el.team.did === did1).sort(compareStandings);
      let div2 = confStats.filter((el) => el.team.did !== did1).sort(compareStandings);
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
          name: this.$t(`teams.${t.team.id}`),
          games: t.stats.games,
          wins: t.stats.winRegular + t.stats.winOvertime + t.stats.winShootout,
          losses: t.stats.loseRegular,
          lossesOT: t.stats.loseOvertime + t.stats.loseShootout,
          points: t.stats.points,
          pointsPercent: getPointsPercentStr(t.stats.points, t.stats.games)
        };
      });
    }
  },
  methods: {
  }
};

</script>

<style lang="less">
  .standings-table {
    margin: 10px;
    table {
      border-collapse: collapse;
      font-size: 16px;
    }
    caption {
      text-align: left;
      padding-left: 20px;
      background: darkgrey;
      line-height: 2em;
    }
    tr {
      border-bottom: 1px solid black;
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
        width: 30px;
        background-color: white;
        &.division-top {
          background-color: green;
        }
        &.wild-card {
          background-color: orange;
        }
      }
      &.number-cell {
        width: 40px;
      }
      &.name-cell {
        width: 180px;
        text-align: left;
        padding-left: 10px;
      }
      &.secondary-cell {
        color: #959595;
      }
    }
  }
</style>
