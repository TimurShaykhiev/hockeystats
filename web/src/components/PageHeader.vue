<template>
  <header class="header">
    <div class="container-row">
      <div class="header__logo container-row" @click="goHome">
        <img src="../../assets/images/logo.svg" class="header__logo-image">
        <h1 class="header__logo-text">Hockstats</h1>
      </div>
      <div class="header__caption" @click="goHome"><h1>{{$t("caption")}}</h1></div>
      <div class="header__change-lang">
        <ul>
          <li @click="setLang('en')">{{$t("chooseLang.eng")}}</li>
          <li @click="setLang('ru')">{{$t("chooseLang.rus")}}</li>
        </ul>
      </div>
    </div>
    <nav class="header__nav-bar container-row">
      <ul>
        <router-link tag="li" :to="{name: 'home'}" class="header__home-link">
          <a>{{$t("navBar.home")}}</a>
        </router-link>
        <router-link tag="li" :to="{name: 'teams'}" class="header__teams-link">
          <a>{{$t("navBar.teams")}}</a>
        </router-link>
        <router-link tag="li" :to="{name: 'skaters'}" class="header__skaters-link">
          <a>{{$t("navBar.skaters")}}</a>
        </router-link>
        <router-link tag="li" :to="{name: 'goalies'}" class="header__goalies-link">
          <a>{{$t("navBar.goalies")}}</a>
        </router-link>
        <router-link tag="li" :to="{name: 'seasons'}" class="header__seasons-link">
          <a>{{$t("navBar.seasons")}}</a>
        </router-link>
        <router-link tag="li" :to="{name: 'ratings'}" class="header__ratings-link">
          <a>{{$t("navBar.ratings")}}</a>
        </router-link>
        <router-link tag="li" :to="{name: 'compare'}" class="header__compare-link">
          <a>{{$t("navBar.compare")}}</a>
        </router-link>
        <hr/>
      </ul>
    </nav>
  </header>
</template>

<script>
import UserSettings from 'Root/userSettings';

export default {
  name: 'page-header',
  i18n: {
    messages: {
      en: {
        caption: 'NHL Hockey Statistics',
        chooseLang: {
          rus: 'Русский',
          eng: 'English'
        }
      },
      ru: {
        caption: 'Хоккейная статистика НХЛ',
        chooseLang: {
          rus: 'Русский',
          eng: 'English'
        }
      }
    }
  },
  methods: {
    setLang(lang) {
      const settings = new UserSettings();
      if (settings.locale !== lang) {
        settings.locale = lang;
        location.reload();
      }
    },
    goHome() {
      this.$router.push({name: 'home'});
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .header {
    align-items: center;
    height: 9rem;
    background: @header-color;
  }
  .header__logo {
    width: 16rem;
    height: 4rem;
    margin: .5rem .5rem .5rem 2.5rem;
    cursor: pointer;
  }
  .header__logo-image {
    width: 6rem;
    height: 4rem;
  }
  .header__logo-text {
    align-self: center;
    font-size: 2.5rem;
    color: @header-text-color;
  }
  .header__caption {
    margin: .5rem 4rem;
    cursor: pointer;
    h1 {
      font-size: 3rem;
      color: @header-text-color;
    }
  }
  .header__nav-bar {
    justify-content: center;
    margin-top: .5rem;
    ul {
      list-style-type: none;
      margin: 0;
      padding: 0;
      overflow: hidden;
      width: 90%;
      li {
        display: inline;
        text-align: center;
        a {
          box-sizing: border-box;
          display: inline-block;
          width: 12%;
          color: @header-text-color;
          text-align: center;
          padding: .5rem;
          text-decoration: none;
        }
      }
      .header__home-link:hover ~ hr {
        margin-left: 2%;
        visibility: visible;
      }
      .header__teams-link:hover ~ hr {
        margin-left: 14%;
        visibility: visible;
      }
      .header__skaters-link:hover ~ hr {
        margin-left: 26%;
        visibility: visible;
      }
      .header__goalies-link:hover ~ hr {
        margin-left: 38%;
        visibility: visible;
      }
      .header__seasons-link:hover ~ hr {
        margin-left: 52%;
        visibility: visible;
      }
      .header__ratings-link:hover ~ hr {
        margin-left: 64%;
        visibility: visible;
      }
      .header__compare-link:hover ~ hr {
        margin-left: 76%;
        visibility: visible;
      }
      hr {
        visibility: hidden;
        height: .25rem;
        width: 10%;
        margin: 0;
        background: @header-text-color;
        border: none;
      }
    }
  }
  .header__change-lang {
    margin: auto .8rem auto auto;
    color: @header-text-color;
    font-size: .75rem;
    ul {
      list-style-type: none;
      margin: .4rem 0;
      padding: 0;
      overflow: hidden;
      text-align: right;
      li {
        cursor: pointer;
        margin: .5rem 0;
      }
    }
  }
</style>
