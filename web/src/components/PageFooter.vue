<template>
  <footer class="footer">
    <nav class="footer__site-map container-row">
      <div class="footer__link-block container-col">
        <ul>
          <router-link tag="li" :to="{name: 'home'}" class="footer__link">
            <a>{{$t("navBar.home")}}</a>
          </router-link>
          <router-link tag="li" :to="{name: 'teams'}" class="footer__link">
            <a>{{$t("navBar.teams")}}</a>
          </router-link>
        </ul>
      </div>
      <div class="footer__link-block container-col">
        <ul>
          <router-link tag="li" :to="{name: 'skaters'}" class="footer__link">
            <a>{{$t("navBar.skaters")}}</a>
          </router-link>
          <router-link tag="li" :to="{name: 'goalies'}" class="footer__link">
            <a>{{$t("navBar.goalies")}}</a>
          </router-link>
        </ul>
      </div>
      <div class="footer__link-block container-col">
        <ul>
          <router-link tag="li" :to="{name: 'compare'}" class="footer__link">
            <a>{{$t("navBar.compare")}}</a>
          </router-link>
        </ul>
      </div>
    </nav>
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
    background: green;
    color: @header-text-color;
    p {
      margin: 1rem;
      text-align: center;
    }
  }
  .footer__site-map {
    height: 5rem;
    margin: 1rem;
    justify-content: space-around;
  }
  .footer__link-block {
    ul {
      list-style-type: none;
      margin: 0;
      padding: 0;
      overflow: hidden;
      li {
        text-align: left;
        a {
          box-sizing: border-box;
          display: inline-block;
          color: @header-text-color;
          text-align: center;
          padding: .5rem;
          text-decoration: none;
        }
      }
    }
  }
</style>
