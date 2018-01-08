<template>
  <footer class="footer">
    <div>{{$t("copyright")}}</div>
  </footer>
</template>

<script>
export default {
  name: 'page-footer',
  i18n: {
    messages: {
      en: {
        copyright: 'Created by Timur.'
      },
      ru: {
        copyright: 'Сделано Тимуром.'
      }
    }
  }
};

</script>

<style lang="less">
  .footer {
    height: 6rem;
    background: green;
  }
</style>
