<template>
  <div class="stats-block container-col">
    <div class="stats-block__caption-block">
      <h2 class="stats-block__caption">{{caption}}</h2>
    </div>
    <div class="stats-block__block container-row">
      <div v-for="el in stats" class="stats-block__item">
        <h1 class="stats-block__value">{{el.value}}</h1>
        <h3 class="stats-block__name">{{el.name}}</h3>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'stats-block',
  props: {
    caption: {type: String, required: true},
    items: {required: true}
  },
  computed: {
    stats() {
      return this.items.map((el) => ({name: el.name.toUpperCase(), value: el.value.toStr()}));
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .stats-block {
    font-family: @header-font;
    margin: 2rem;
    border: 1px solid @border-color;
  }
  .stats-block__caption-block {
    color: @header-text-color;
    background: @header-color;
    height: 2.5em;
    padding-left: 1rem;
    .stats-block__caption {
      margin: .4rem 0;
    }
  }
  .stats-block__block {
    justify-content: space-around;
  }
  .stats-block__item {
    margin: .5rem;
    max-width: 12rem;
    min-width: 10rem;
    height: 8rem;
    text-align: center;
  }
  .stats-block__value {
    font-size: 2rem;
    margin: 1rem 0;
  }
  .stats-block__name {
    color: @header-color;
    font-size: 1rem;
    margin: 0 .5rem;
  }
</style>
