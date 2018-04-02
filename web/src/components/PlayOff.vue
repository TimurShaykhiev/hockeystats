<template>
  <div class="play-off">
    <p v-if="infoMessage.show" class="play-off__message">{{infoMessage.msg}}</p>
    <div class="play-off__container container-row">
      <div v-for="round in dataSet" class="play-off__round container-col">
        <div v-for="pair in round" :class="pair.blockClass">
          <table v-if="pair.notEmpty">
            <tr v-for="team in pair.teams">
              <td class="play-off__team-name-cell">
                <router-link :to="{name: 'team', params: {id: team.id}}">{{team.name}}</router-link>
              </td>
              <td class="play-off__score-cell">{{team.wins}}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';

const ROUND_MAX = 4;

export default {
  name: 'play-off',
  props: {
    currentSeason: {type: Boolean, default: true}
  },
  i18n: {
    messages: {
      en: {
        playOff: {
          tooEarlyMsg: 'It is too early for Playoff information.',
          notFinalMsg: 'These Playoff pairs are not final.'
        }
      },
      ru: {
        playOff: {
          tooEarlyMsg: 'До плэй-офф ещё далеко.',
          notFinalMsg: 'Пары плэй-офф еще могут измениться.'
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
    infoMessage() {
      let result = {show: false, msg: ''};
      let season = this.currentSeason ?
        this.$store.state.season.currentSeason : this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        let playOff = this.$store.getters.getPlayOff(season);
        if (playOff !== null) {
          if (playOff.rounds.length === 0) {
            result.show = true;
            result.msg = this.$t('playOff.tooEarlyMsg');
          } else if (Date.now() < season.poStart) {
            result.show = true;
            result.msg = this.$t('playOff.notFinalMsg');
          }
        }
      }
      return result;
    },

    dataSet() {
      let season = this.currentSeason ?
        this.$store.state.season.currentSeason : this.$store.state.season.selectedSeason;
      if (season.id === undefined) {
        return [];
      }
      let allTeams = this.$store.getters.getAllTeams(season);
      let playOff = this.$store.getters.getPlayOff(season);
      if (allTeams === null || playOff === null) {
        this.requestData(season);
        return [];
      }
      allTeams = allTeams.teams;
      const poRoundsTotal = playOff.rounds.length;

      let createLinkBlock = (level) => {
        return {
          notEmpty: false,
          blockClass: `play-off__link-block play-off__link-block--${level}`
        };
      };
      let createPair = (pair) => {
        if (pair === undefined) {
          return {
            notEmpty: true,
            blockClass: 'play-off__pair',
            teams: [{id: 0, name: '', wins: ''}, {id: 0, name: '', wins: ''}]
          };
        }
        const complete = pair.tid1 !== 0 && pair.tid2 !== 0;
        return {
          notEmpty: true,
          blockClass: 'play-off__pair',
          teams: [{
            id: pair.tid1,
            name: pair.tid1 !== 0 ? allTeams[pair.tid1].name : '',
            wins: complete ? pair.wins1 : ''
          }, {
            id: pair.tid2,
            name: pair.tid2 !== 0 ? allTeams[pair.tid2].name : '',
            wins: complete ? pair.wins2 : ''
          }]
        };
      };

      let result = [];
      let linkBlocksNum = 4;
      for (let rNum = 0; rNum < ROUND_MAX; ++rNum) {
        let round = [];
        const pairsNum = Math.pow(2, 3-rNum);
        let roundData;
        let roundDataIdx = -1;

        if (rNum < poRoundsTotal) {
          roundData = playOff.rounds[rNum];
          roundDataIdx = 0;
        }
        for (let i = 0; i < pairsNum; ++i) {
          if (roundDataIdx > -1 && roundDataIdx < roundData.length) {
            let pair = roundData[roundDataIdx];
            if (pair.num === i) {
              round.push(createPair(pair));
              roundDataIdx += 1;
            } else {
              round.push(createPair());
            }
          } else {
            round.push(createPair());
          }
        }
        result.push(round);

        if (linkBlocksNum >= 1) {
          let linkBlocks = [];
          for (let i = 0; i < linkBlocksNum; ++i) {
            linkBlocks.push(createLinkBlock(rNum));
          }
          result.push(linkBlocks);
          linkBlocksNum = linkBlocksNum / 2;
        }
      }
      return result;
    }
  },
  methods: {
    requestData(season) {
      let reqParams = new SeasonRequestParams(this.$store, season.id, season.regular);
      this.$store.dispatch('getAllTeams', {reqParams: reqParams});
      this.$store.dispatch('getTeamsPlayOff', {reqParams: reqParams});
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  @pair-block-height: 4rem;
  @border: 1px solid @border-color;

  .play-off__message {}
  .play-off__container {
    width: 100%;
  }
  .play-off__round {
    .desktop({
      height: @pair-block-height * 10;
    });
    .small-desktop({
      height: @pair-block-height * 15;
    });
    min-width: 5%;
    justify-content: space-around;
    &:nth-child(even) {
      width: 50px;
    }
  }
  .play-off__pair {
    z-index: 2;
    background-color: #fff;
    border: 2px solid @border-color;
    border-radius: 4px;
    .desktop({
      width: 14rem;
      height: @pair-block-height;
    });
    .small-desktop({
      width: 10rem;
      height: @pair-block-height * 1.5;
    });
    table {
      border: none;
      width: 100%;
      height: 100%;
    }
  }
  .play-off__team-name-cell {
    width: 90%;
    padding-left: .5rem;
    a {
      color: black;
      text-decoration: none;
    }
  }
  .play-off__score-cell {
    width: 10%;
    text-align: center;
  }
  .play-off__link-block {
    border-top: @border;
    border-bottom: @border;
    border-right: @border;
    width: 90px;
    z-index: 1;
  }
  .play-off__link-block--0 {
    .desktop({
      height: 6rem;
    });
    .small-desktop({
      height: 9rem;
    });
  }
  .play-off__link-block--1 {
    .desktop({
      height: 10rem;
    });
    .small-desktop({
      height: 15rem;
    });
  }
  .play-off__link-block--2 {
    .desktop({
      height: 20rem;
    });
    .small-desktop({
      height: 30rem;
    });
  }
</style>
