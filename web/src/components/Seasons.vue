<template>
  <div class="seasons">
    <h1 class="seasons__title">{{$t('title')}}</h1>
    <div class="seasons__season-picker container-row">
      <season-picker type="all"/>
    </div>
  </div>
</template>

<script>

export default {
  name: 'seasons',
  i18n: {
    messages: {
      en: {
        title: 'Seasons'
      },
      ru: {
        title: 'Сезоны'
      }
    }
  },
  created() {
  },
  computed: {
  },
  methods: {
  }
};

</script>

<style lang="less">
  .seasons__title {
    text-align: center;
    margin: 1rem 0;
  }
  .seasons__season-picker {
    justify-content: flex-end;
    padding: 0 2rem;
    margin: 1rem 0;
  }
</style>
