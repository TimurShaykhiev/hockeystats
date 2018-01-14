<template>
  <div class="player-personal-info container-col">
    <div class="player-personal-info__title container-row">
      <img :src="logoUrl" class="player-personal-info__logo">
      <h1 class="player-personal-info__player-name">{{name}}</h1>
    </div>
    <hr class="player-personal-info__divider"/>
    <div class="player-personal-info__vitals container-row">
      <div v-for="el in vitals" class="player-personal-info__item">
        <h1 class="player-personal-info__value">{{el.value}}</h1>
        <h3 class="player-personal-info__name">{{el.name}}</h3>
      </div>
    </div>
    <hr class="player-personal-info__divider"/>
  </div>
</template>

<script>

export default {
  name: 'player-personal-info',
  props: {
    id: {type: Number, required: true},
    name: {type: String, required: true},
    pos: {type: String, required: true},
    tid: {type: Number, required: true},
    shoots: {type: String, required: true},
    height: {type: String, required: true},
    weight: {type: Number, required: true},
    age: {type: Number, required: true}
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
  data() {
    return {};
  },
  computed: {
    logoUrl() {
      return `images/team${this.tid}.svg`;
    },

    vitals() {
      return [
        {name: this.$t('playerPersonalInfo.position'), value: this.$t(`position.${this.pos}`)},
        {name: this.$t('playerPersonalInfo.shoots'), value: this.$t(`shootsType.${this.shoots}`)},
        {name: this.$t('playerPersonalInfo.height'), value: this.height},
        {name: this.$t('playerPersonalInfo.weight'), value: this.weight},
        {name: this.$t('playerPersonalInfo.age'), value: this.age}
      ];
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
    padding: 0 3rem;
  }
  .player-personal-info__logo {
    width: 10rem;
    height: 10rem;
  }
  .player-personal-info__player-name {
    font-size: 4rem;
    margin: 0 0 0 2.5rem;
  }
  .player-personal-info__vitals {
    justify-content: space-around;
  }
  .player-personal-info__item {
    margin: .5rem;
    max-width: 8rem;
    min-width: 6rem;
    height: 3rem;
    text-align: center;
  }
  .player-personal-info__value {
    font-size: 1.25rem;
  }
  .player-personal-info__name {
    font-size: 1rem;
    margin: 0 .5rem;
  }
  .player-personal-info__divider {
    background: @border-color;
    height: .25rem;
    width: 95%;
    margin: 1rem 2.5%;
    border: none;
  }
</style>
