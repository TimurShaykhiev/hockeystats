<template>
  <div class="wrapper container-col">
    <page-header></page-header>
    <div class="top-banner"></div>
    <div class="container-row">
      <div class="main-content">
        <router-view></router-view>
      </div>
      <div class="side-banner"></div>
    </div>
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

<style lang="less" scoped>
  .top-banner {
    height: 5px;
    background: lightgrey;
    margin: 5px;
  }
  .main-content {
    flex: 5 5 0px;
    margin: 10px;
  }
  .side-banner {
    background: lightgrey;
    max-width: 120px;
    min-width: 120px;
    flex: 1 1 0px;
    margin: 5px;
  }
</style>
