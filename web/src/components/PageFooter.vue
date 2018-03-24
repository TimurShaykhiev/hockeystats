<template>
  <footer class="footer">
    <p>&copy; {{copyrightYears}} hockstats</p>
  </footer>
</template>

<script>
export default {
  name: 'page-footer',
  data() {
    let year = (new Date()).getFullYear();
    return {
      copyrightYears: `2017-${year}`
    };
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .footer {
    height: 3rem;
    background: green;
    color: @header-text-color;
    p {
      margin: 1rem 2rem;
    }
  }
</style>
