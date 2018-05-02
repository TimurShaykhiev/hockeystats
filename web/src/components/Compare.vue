<template>
  <div class="compare">
    <div class="compare__season-picker container-row">
      <season-picker type="all"/>
    </div>
    <nav class="compare__select-type container-row">
      <ul>
        <li class="compare__teams-link" :class="{'compare__link--selected': compareType === 0}">
          <a @click.prevent="typeSelected" data-compareType="0">{{$t("compareList.teams")}}</a>
        </li>
        <li class="compare__skaters-link" :class="{'compare__link--selected': compareType === 1}">
          <a @click.prevent="typeSelected" data-compareType="1">{{$t('compareList.skaters')}}</a>
        </li>
        <li class="compare__goalies-link" :class="{'compare__link--selected': compareType === 2}">
          <a @click.prevent="typeSelected" data-compareType="2">{{$t('compareList.goalies')}}</a>
        </li>
        <hr/>
      </ul>
    </nav>
    <div class="compare__selectors-container container-col">
      <v-select class="compare__selector" v-model="leftSelectedObj" :options="itemList" label="name"
                :placeholder="selectBoxPlaceholder"/>
      <h1 class="compare__selectors-vs">VS</h1>
      <v-select class="compare__selector" v-model="rightSelectedObj" :options="itemList" label="name"
                :placeholder="selectBoxPlaceholder"/>
    </div>
    <div class="compare__button-container container-row">
      <button class="compare__button button" @click="compareClicked" :disabled="compareDisabled">
        {{$t('compareButton')}}
      </button>
    </div>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import Utils from 'Root/utils';

const COMPARE_TYPE_TEAM = 0;
const COMPARE_TYPE_SKATER = 1;
const COMPARE_TYPE_GOALIE = 2;

export default {
  name: 'compare',
  i18n: {
    messages: {
      en: {
        compareList: {
          title: 'Compare',
          teams: 'Teams',
          skaters: 'Skaters',
          goalies: 'Goaltenders'
        },
        compareButton: 'Compare'
      },
      ru: {
        compareList: {
          title: 'Сравнить',
          teams: 'Команды',
          skaters: 'Игроки',
          goalies: 'Вратари'
        },
        compareButton: 'Сравнить'
      }
    }
  },
  data() {
    return {
      leftSelectedObj: null,
      rightSelectedObj: null,
      compareType: 0
    };
  },
  created() {
    this.requestItems();
  },
  computed: {
    selectBoxPlaceholder() {
      let result = this.$t('itemSelectorPlaceholder.team');
      if (this.compareType === COMPARE_TYPE_SKATER) {
        result = this.$t('itemSelectorPlaceholder.skater');
      } else if (this.compareType === COMPARE_TYPE_GOALIE) {
        result = this.$t('itemSelectorPlaceholder.goalie');
      }
      return result;
    },

    compareDisabled() {
      const leftObj = this.leftSelectedObj;
      const rightObj = this.rightSelectedObj;
      const season = this.$store.state.season.selectedSeason;
      return leftObj === null || rightObj === null || season.id === undefined || leftObj.id === rightObj.id;
    },

    itemList() {
      let season = this.$store.state.season.selectedSeason;
      let getterName = 'getAllTeamsForSeason';
      if (this.compareType === COMPARE_TYPE_SKATER) {
        getterName = 'getAllSkaters';
      } else if (this.compareType === COMPARE_TYPE_GOALIE) {
        getterName = 'getAllGoalies';
      }
      let items = this.$store.getters[getterName](season);
      if (items === null) {
        this.requestItems();
        this.leftSelectedObj = null;
        this.rightSelectedObj = null;
        return [];
      }
      let result = [];
      if (this.compareType === COMPARE_TYPE_TEAM) {
        result = Object.keys(items.teams).map((k) => ({id: items.teams[k].id, name: items.teams[k].name}));
      } else {
        result = items.players;
      }
      return Utils.sortBy(result, (e) => e.name);
    }
  },
  methods: {
    typeSelected(event) {
      const type = parseInt(event.target.getAttribute('data-compareType'));
      if (this.compareType !== type) {
        this.compareType = type;
        this.leftSelectedObj = null;
        this.rightSelectedObj = null;
      }
    },

    compareClicked() {
      const leftObj = this.leftSelectedObj;
      const rightObj = this.rightSelectedObj;
      let routeName = 'teamsCompare';
      if (this.compareType === COMPARE_TYPE_SKATER) {
        routeName = 'skatersCompare';
      } else if (this.compareType === COMPARE_TYPE_GOALIE) {
        routeName = 'goaliesCompare';
      }
      this.$router.push({name: routeName, params: {id1: leftObj.id, id2: rightObj.id}});
    },

    requestItems() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id === undefined) {
        return;
      }
      let action = 'getAllTeamsForSeason';
      if (this.compareType === COMPARE_TYPE_SKATER) {
        action = 'getAllSkaters';
      } else if (this.compareType === COMPARE_TYPE_GOALIE) {
        action = 'getAllGoalies';
      }
      this.$store.dispatch(action, {reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)});
    }
  }
};

</script>

<style lang="less">
  @selector-text-color: black;

  .compare__season-picker {
    justify-content: flex-end;
    padding: 0 2rem;
    margin: 1rem 0;
  }
  .compare__select-type {
    font-size: 1.3rem;
  }
  .compare__select-type {
    justify-content: center;
    margin-top: .5rem;
    ul {
      list-style-type: none;
      margin: 0;
      padding: 0;
      overflow: hidden;
      width: 80%;
      text-align: center;
      li {
        display: inline;
        text-align: center;
        font-weight: normal;
        a {
          box-sizing: border-box;
          display: inline-block;
          width: 25%;
          color: @selector-text-color;
          text-align: center;
          padding: .5rem;
          text-decoration: none;
          cursor: pointer;
        }
      }
      .compare__teams-link:hover ~ hr {
        margin-left: 15%;
        visibility: visible;
      }
      .compare__skaters-link:hover ~ hr {
        margin-left: 40%;
        visibility: visible;
      }
      .compare__goalies-link:hover ~ hr {
        margin-left: 65%;
        visibility: visible;
      }
      .compare__link--selected {
        font-weight: bold;
      }
      hr {
        visibility: hidden;
        height: .25rem;
        width: 20%;
        margin: 0;
        background: @selector-text-color;
        border: none;
      }
    }
  }
  .compare__selectors-container {
    justify-content: center;
    margin: 2rem 25%;
    width: 50%;

    .compare__selectors-vs {
      text-align: center;
    }
    .compare__selector {
      margin: 1rem 0;
    }
  }
  .compare__button-container {
    justify-content: center;
  }
</style>
