<template>
  <div class="wrapper container-col">
    <page-header></page-header>
    <page-footer></page-footer>
  </div>
</template>

<script>
import PageHeader from 'Components/PageHeader';
import PageFooter from 'Components/PageFooter';

export default {
  name: 'app',
  components: {PageHeader, PageFooter}
};

</script>

<style lang="less">
</style>
