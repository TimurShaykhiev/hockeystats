<template>
  <div class="season-top-result container-col">
    <div class="season-top-result__caption-block container-col">
      <h3 class="season-top-result__caption">{{caption}}</h3>
    </div>
    <h1 class="season-top-result__value" :class="statQualityClass">{{statValue}}</h1>
    <div v-if="showTeams" class="season-top-result__names">
      <router-link v-for="el in names" :key="el.id" :to="{name: el.routeName, params: {id: el.id}}"
                   class="season-top-result__main-name">
        {{el.name}}
      </router-link>
    </div>
    <div v-else class="season-top-result__names">
      <div v-for="el in names" :key="el.id">
        <router-link :to="{name: el.routeName, params: {id: el.id}}" class="season-top-result__main-name">
          {{el.name}} ({{$t(`playerPosition.${el.pos}`)}})
        </router-link>
        <span class="season-top-result__sec-name">{{el.team}}</span>
      </div>
    </div>
  </div>
</template>

<script>

const TYPE_TEAM = 'team';

export default {
  name: 'season-top-result',
  props: {
    type: {type: String, required: true},
    label: {type: String, required: true},
    value: {required: true},
    names: {type: Array, required: true},
    best: {type: Boolean, default: true}
  },
  data() {
    return {
      caption: this.label.toUpperCase(),
      statValue: this.value.toStr(),
      showTeams: this.type === TYPE_TEAM
    };
  },
  computed: {
    statQualityClass() {
      return this.best ? 'good-stat' : 'bad-stat';
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .season-top-result {
    margin: 1rem;
    align-items: center;
    text-align: center;
    width: 13rem;
  }
  .season-top-result__caption-block {
    justify-content: center;
    color: @header-text-color;
    background: @header-color;
    height: 3rem;
    width: 100%;
  }
  .season-top-result__caption {
    font-size: 1rem;
    margin: 0 .2rem;
  }
  .season-top-result__value {
    font-size: 3rem;
    margin: 1rem 0;
  }
  .season-top-result__main-name {
    display: block;
    font-size: 1.2rem;
    color: @main-text-color;
    text-decoration: none;
  }
  .season-top-result__sec-name {
    display: block;
    font-size: .9rem;
    margin-bottom: .5rem;
  }
  .good-stat {
    color: @good-stat-color;
  }
  .bad-stat {
    color: @bad-stat-color;
  }
  .season-top-result__names {}
</style>
