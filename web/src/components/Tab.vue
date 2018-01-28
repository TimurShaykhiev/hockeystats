<template>
  <section v-if="isActive" class="tab-component">
    <slot/>
  </section>
</template>

<script>

export default {
  props: {
    name: {type: String, required: true},
    prefix: {default: ''},
    suffix: {default: ''},
    isDisabled: {type: Boolean, default: false}
  },
  data() {
    return {
      // to make tab id unique
      id: this.name + Math.floor(Math.random() * 1000).toString(),
      isActive: false
    };
  },
  computed: {
    header() {
      return this.prefix + this.name + this.suffix;
    }
  }
};

</script>

<style lang="less">
</style>
