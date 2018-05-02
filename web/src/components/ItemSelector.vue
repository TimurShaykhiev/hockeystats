<template>
  <div class="item-selector container-row">
    <v-select class="item-selector__selector" v-model="selectedObj" :options="itemList" label="name"
              :placeholder="selectBoxPlaceholder"/>
    <button class="item-selector__button button button--small" @click="openClicked" :disabled="buttonsDisabled">
      {{$t('openButtonLabel')}}
    </button>
    <button class="item-selector__button button button--small" @click="compareClicked" :disabled="buttonsDisabled">
      {{$t('compareButtonLabel')}}
    </button>
  </div>
</template>

<script>
import {SeasonRequestParams} from 'Store/types';
import Utils from 'Root/utils';

const TYPE_TEAM = 'team';
const TYPE_SKATER = 'skater';
const TYPE_GOALIE = 'goalie';

export default {
  name: 'item-selector',
  props: {
    type: {type: String, required: true}
  },
  i18n: {
    messages: {
      en: {
        compareButtonLabel: 'Compare',
        openButtonLabel: 'Open'
      },
      ru: {
        compareButtonLabel: 'Сравнить',
        openButtonLabel: 'Открыть'
      }
    }
  },
  data() {
    return {
      selectedObj: null
    };
  },
  created() {
    this.requestItems();
  },
  computed: {
    selectBoxPlaceholder() {
      let result = this.$t('itemSelectorPlaceholder.team');
      if (this.type === TYPE_SKATER) {
        result = this.$t('itemSelectorPlaceholder.skater');
      } else if (this.type === TYPE_GOALIE) {
        result = this.$t('itemSelectorPlaceholder.goalie');
      }
      return result;
    },

    buttonsDisabled() {
      const season = this.$store.state.season.selectedSeason;
      return this.selectedObj === null || season.id === undefined ||
             parseInt(this.$route.params.id) === this.selectedObj.id;
    },

    itemList() {
      let season = this.$store.state.season.selectedSeason;
      let getterName = 'getAllTeamsForSeason';
      if (this.type === TYPE_SKATER) {
        getterName = 'getAllSkaters';
      } else if (this.type === TYPE_GOALIE) {
        getterName = 'getAllGoalies';
      }
      let items = this.$store.getters[getterName](season);
      if (items === null) {
        this.requestItems();
        this.selectedObj = null;
        return [];
      }
      let result = [];
      if (this.type === TYPE_TEAM) {
        result = Object.keys(items.teams).map((k) => ({id: items.teams[k].id, name: items.teams[k].name}));
      } else {
        result = items.players;
      }
      return Utils.sortBy(result, (e) => e.name);
    }
  },
  methods: {
    openClicked() {
      let routeName = 'team';
      if (this.type === TYPE_SKATER) {
        routeName = 'skater';
      } else if (this.type === TYPE_GOALIE) {
        routeName = 'goalie';
      }
      const selectedId = this.selectedObj.id;
      this.selectedObj = null;
      this.$router.push({name: routeName, params: {id: selectedId}});
    },

    compareClicked() {
      let routeName = 'teamsCompare';
      if (this.type === TYPE_SKATER) {
        routeName = 'skatersCompare';
      } else if (this.type === TYPE_GOALIE) {
        routeName = 'goaliesCompare';
      }
      const selectedId = this.selectedObj.id;
      this.selectedObj = null;
      this.$router.push({name: routeName, params: {id1: this.$route.params.id, id2: selectedId}});
    },

    requestItems() {
      let season = this.$store.state.season.selectedSeason;
      if (season.id === undefined) {
        return;
      }
      let action = 'getAllTeamsForSeason';
      if (this.type === TYPE_SKATER) {
        action = 'getAllSkaters';
      } else if (this.type === TYPE_GOALIE) {
        action = 'getAllGoalies';
      }
      this.$store.dispatch(action, {reqParams: new SeasonRequestParams(this.$store, season.id, season.regular)});
    }
  }
};

</script>

<style lang="less">
  .item-selector {
    align-items: center;
  }
  .item-selector__selector {
    width: 50%;
  }
</style>
