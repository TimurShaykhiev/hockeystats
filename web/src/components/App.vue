<template>
  <div class="wrapper container-col">
    <page-header/>
    <div class="main-area container-row">
      <div class="main-content">
        <router-view/>
      </div>
    </div>
    <page-footer/>
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
  .main-area {
    flex: 1;
  }
  .main-content {
    width: 100%;
    margin: 1rem 3rem;
  }
</style>
