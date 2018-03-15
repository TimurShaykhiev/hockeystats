<template>
  <div class="player-personal-info container-col">
    <div class="player-personal-info__title container-row">
      <img :src="logoUrl" class="player-personal-info__logo" :class="layoutClasses">
      <div class="player-personal-info__player-info container-col">
        <h1 class="player-personal-info__player-name" :class="playerNameClasses">{{playerInfo.name}}</h1>
        <h3 class="player-personal-info__team-name" :class="layoutClasses">{{teamName}}</h3>
      </div>
    </div>
    <hr class="player-personal-info__divider"/>
    <div class="player-personal-info__vitals container-row">
      <div v-for="el in vitals" class="player-personal-info__item" :class="layoutClasses">
        <h1 class="player-personal-info__value" :class="layoutClasses">{{el.value}}</h1>
        <h3 class="player-personal-info__name" :class="layoutClasses">{{el.name}}</h3>
      </div>
    </div>
    <hr class="player-personal-info__divider"/>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';

export default {
  name: 'player-personal-info',
  props: {
    playerInfo: {required: true},
    fullWidth: {type: Boolean, default: true},
    comparePosition: {type: String}
  },
  i18n: {
    messages: {
      en: {
        playerPersonalInfo: {
          position: 'POSITION',
          shoots: 'SHOOTS',
          height: 'HEIGHT',
          weight: 'WEIGHT',
          age: 'AGE'
        },
        shootsType: {
          L: 'LEFT',
          R: 'RIGHT'
        },
        position: {
          C: 'CENTER',
          R: 'RIGHT WING',
          L: 'LEFT WING',
          D: 'DEFENCEMAN',
          G: 'GOALTENDER'
        }
      },
      ru: {
        playerPersonalInfo: {
          position: 'АМПЛУА',
          shoots: 'ХВАТ',
          height: 'РОСТ',
          weight: 'ВЕС',
          age: 'ВОЗРАСТ'
        },
        shootsType: {
          L: 'ЛЕВЫЙ',
          R: 'ПРАВЫЙ'
        },
        position: {
          C: 'ЦЕНТР. НАП.',
          R: 'ПРАВЫЙ НАП.',
          L: 'ЛЕВЫЙ НАП.',
          D: 'ЗАЩИТНИК',
          G: 'ВРАТАРЬ'
        }
      }
    }
  },
  created() {
    this.requestAllTeams();
  },
  data() {
    return {
      playerNameClasses: {
        'full-width': this.fullWidth,
        'compare--left': this.comparePosition === 'left',
        'compare--right': this.comparePosition === 'right'
      },
      layoutClasses: {
        'full-width': this.fullWidth
      }
    };
  },
  computed: {
    logoUrl() {
      return `images/team${this.playerInfo.tid}.svg`;
    },

    teamName() {
      let season = this.$store.state.season.selectedSeason;
      let allTeams = this.$store.getters.getAllTeams(season);
      if (allTeams === null) {
        this.requestAllTeams();
        return '';
      }
      return allTeams.teams[this.playerInfo.tid].name;
    },

    vitals() {
      return [
        {name: this.$t('playerPersonalInfo.position'), value: this.$t(`position.${this.playerInfo.pos}`)},
        {name: this.$t('playerPersonalInfo.shoots'), value: this.$t(`shootsType.${this.playerInfo.shoots}`)},
        {name: this.$t('playerPersonalInfo.height'), value: this.playerInfo.height},
        {name: this.$t('playerPersonalInfo.weight'), value: this.playerInfo.weight},
        {name: this.$t('playerPersonalInfo.age'), value: this.playerInfo.age}
      ];
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
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .player-personal-info {
    margin-bottom: 1rem;
  }
  .player-personal-info__title {
    align-items: center;
    padding: 0 1rem;
    min-height: 10rem;
    &.full-width {
      padding: 0 3rem;
    }
  }
  .player-personal-info__logo {
    flex: 1;
    width: 8rem;
    height: 8rem;
    &.full-width {
      width: 10rem;
      height: 10rem;
    }
  }
  .player-personal-info__player-info {
     margin: 0 0 0 2.5rem;
     flex: 4;

    .player-personal-info__player-name {
      font-size: 3rem;
      &.full-width {
        font-size: 4rem;
      }
    }
    .player-personal-info__team-name {
      font-size: 1.4rem;
      margin-top: 1rem;
    }
  }
  .player-personal-info__vitals {
    justify-content: space-around;
  }
  .player-personal-info__item {
    margin: 0 .5rem;
    max-width: 8rem;
    min-width: 6rem;
    text-align: center;
    &.full-width {
      margin: .5rem;
    }
  }
  .player-personal-info__value {
    font-size: 1.25rem;
    &.full-width {
      font-size: 1.25rem;
    }
  }
  .player-personal-info__name {
    font-size: 1rem;
    margin: 0 .5rem;
    &.full-width {
      font-size: 1rem;
    }
  }
  .player-personal-info__divider {
    background: @border-color;
    height: .25rem;
    width: 95%;
    margin: .75rem 2.5%;
    border: none;
    &.full-width {
      margin: 1rem 2.5%;
    }
  }
</style>
