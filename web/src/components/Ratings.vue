<template>
  <div class="ratings">
    <h1 class="ratings__title">{{$t('title')}}</h1>
    <div class="ratings__season-picker container-row">
      <season-picker type="all"/>
    </div>
    <div class="ratings__main-container container-row">
      <div class="ratings__menu">
        <ul class="ratings__menu-list">
          <li v-for="el in menuList" :class="{'ratings__menu-list--selected': el.selected}" @click="el.handler">
            {{el.name}}
          </li>
        </ul>
      </div>
      <div class="ratings__rating-container">
        <h2 class="ratings__rating-name">{{rating.name}}</h2>
        <p class="ratings__rating-description">{{rating.description}}</p>
        <div v-if="rating.scorerDuos">
          <div v-for="d in rating.data">
            <div class="ratings__scorer-duo container-row">
              <rating-player-info class="ratings__scorer-duo-player-info" v-bind="d.player1"></rating-player-info>
              <div class="ratings__scorer-duo-goals">
                <span>{{d.goals}}</span>
              </div>
              <rating-player-info class="ratings__scorer-duo-player-info" v-bind="d.player2"></rating-player-info>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import CompUtils from 'Components/utils';
import RatingPlayerInfo from 'Components/RatingPlayerInfo';

const RATING_SCORER_DUOS = 1;

export default {
  name: 'ratings',
  components: {RatingPlayerInfo},
  i18n: {
    messages: {
      en: {
        title: 'Ratings',
        menu: {
          scorerDuos: 'Scorer duos'
        },
        names: {
          scorerDuos: 'Best scorer duos. '
        },
        description: {
          scorerDuos: 'Players are sorted by number of goals scored together (scorer and 1st assistant). ' +
                      'Rating shows player points and amount of points earned in duo.'
        }
      },
      ru: {
        title: 'Рейтинги',
        menu: {
          scorerDuos: 'Пара нападающих'
        },
        names: {
          scorerDuos: 'Самые результативные пары нападающих. '
        },
        description: {
          scorerDuos: 'Игроки отсортированы по количеству голов, забитых вместе (автор и 1-й ассистент). ' +
                      'Рейтинг показывает количество очков у игрока и долю очков, заработанных в паре.'
        }
      }
    }
  },
  data() {
    return {
      selectedRating: RATING_SCORER_DUOS
    };
  },
  created() {
    this.requestAllTeams();
  },
  computed: {
    menuList() {
      return [{
          name: this.$t('menu.scorerDuos'),
          handler: this.scorerDuos,
          selected: this.selectedRating === RATING_SCORER_DUOS
        }
      ];
    },

    rating() {
      let selSeason = this.$store.state.season.selectedSeason;
      if (this.selectedRating === RATING_SCORER_DUOS) {
        let ratingData = this.$store.getters.getRating('scorerDuos', selSeason);
        if (ratingData === null) {
          this.requestRatingData('getScorerDuos');
          return {};
        }
        let allTeams = this.$store.getters.getAllTeams(selSeason);
        if (allTeams === null) {
          this.requestAllTeams();
          return {};
        }
        allTeams = allTeams.teams;
        let data = ratingData.rating.map((el) => {
          const player1 = ratingData.players[el.pid1];
          const player2 = ratingData.players[el.pid2];
          return {
            player1: {
              name: player1.name,
              team: allTeams[player1.tid].name,
              value: el.pp1,
              sharedValue: el.g,
              showValueBar: true,
              sharedValueBarRight: true
            },
            player2: {
              name: player2.name,
              team: allTeams[player2.tid].name,
              value: el.pp2,
              sharedValue: el.g,
              showValueBar: true
            },
            goals: el.g
          };
        });
        return {
          scorerDuos: true,
          name: this.$t('names.scorerDuos') + CompUtils.seasonToStr(selSeason),
          description: this.$t('description.scorerDuos'),
          data: data
        };
      }
      return {};
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

    requestRatingData(ratingName) {
      let season = this.$store.state.season.selectedSeason;
      if (season.id !== undefined) {
        this.$store.dispatch(ratingName, {
          reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)
        });
      }
    },

    scorerDuos() {
      if (this.selectedRating !== RATING_SCORER_DUOS) {
        this.selectedRating = RATING_SCORER_DUOS;
      }
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .ratings__title {
    text-align: center;
    margin: 1rem 0;
  }
  .ratings__season-picker {
    justify-content: flex-end;
    padding: 0 2rem;
    margin: 1rem 0;
  }
  .ratings__main-container {
    margin-top: 2rem;
  }
  .ratings__menu {
    flex: 1;
    margin-top: 2rem;
  }
  .ratings__menu-list {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    li {
      display: block;
      color: @menu-text-color;
      padding: .5rem;
      &:hover {
        cursor: pointer;
        color: @menu-hover-text-color;
        background-color: @menu-hover-background-color;
      }
      &.ratings__menu-list--selected {
        color: @menu-selected-text-color;
        background-color: @menu-selected-background-color;
      }
    }
  }
  .ratings__rating-container {
    flex: 3;
    padding: 0 1rem;
  }
  .ratings__rating-name {
    text-align: center;
    margin-bottom: 2rem;
  }
  .ratings__rating-description {
    padding: 0 2rem;
  }
  .ratings__scorer-duo {
    justify-content: center;
    margin-top: 4rem;
  }
  .ratings__scorer-duo-player-info {
    flex: 2;
    text-align: center;
  }
  .ratings__scorer-duo-goals {
    flex: 1;
    text-align: center;
    span {
      display: block;
      font-size: 2rem;
    }
  }
</style>
