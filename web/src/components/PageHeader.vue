<template>
  <header class="header">
    <div class="container-row">
      <div class="header__logo" @click="goHome">Logo</div>
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
        caption: 'Hockey statistics',
        navBar: {
          home: 'Home',
          teams: 'Teams',
          skaters: 'Skaters',
          goalies: 'Goaltenders'
        },
        chooseLang: {
          rus: 'Русский',
          eng: 'English'
        }
      },
      ru: {
        caption: 'Хоккейная статистика',
        navBar: {
          home: 'Главная',
          teams: 'Команды',
          skaters: 'Игроки',
          goalies: 'Вратари'
        },
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
    width: 8rem;
    height: 4rem;
    margin: .5rem .5rem .5rem 1.5rem;
    background: darkblue;
    color: @header-text-color;
    cursor: pointer;
  }
  .header__caption {
    margin-left: 4rem;
    font-size: 1.5rem;
    color: @header-text-color;
    cursor: pointer;
  }
  .header__nav-bar {
    justify-content: center;
    margin-top: .5rem;
    ul {
      list-style-type: none;
      margin: 0;
      padding: 0;
      overflow: hidden;
      width: 80%;
      li {
        display: inline;
        text-align: center;
        a {
          box-sizing: border-box;
          display: inline-block;
          width: 24%;
          color: @header-text-color;
          text-align: center;
          padding: .5rem;
          text-decoration: none;
        }
      }
      .header__home-link:hover ~ hr {
        margin-left: 5%;
        visibility: visible;
      }
      .header__teams-link:hover ~ hr {
        margin-left: 30%;
        visibility: visible;
      }
      .header__skaters-link:hover ~ hr {
        margin-left: 55%;
        visibility: visible;
      }
      .header__goalies-link:hover ~ hr {
        margin-left: 77%;
        visibility: visible;
      }
      hr {
        visibility: hidden;
        height: .25rem;
        width: 15%;
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
      }
    }
  }
</style>
