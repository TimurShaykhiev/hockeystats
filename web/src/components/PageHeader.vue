<template>
  <header class="header container-row">
    <div class="header__logo">
    </div>
    <h1 class="header__caption">Hockey stats</h1>
  </header>
</template>

<script>
export default {
  name: 'page-header'
};

</script>

<style lang="less">
  .header {
    align-items: center;
    height: 200px;
    background: yellow;
  }
  .header__logo {
    width: 150px;
    height: 150px;
    margin: 20px;
  }
  .header__caption {
    margin-left: 50px;
    font-size: 80px;
  }
</style>
