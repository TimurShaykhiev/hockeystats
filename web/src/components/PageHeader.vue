<template>
  <header class="header container-row">
    <div class="header__logo" @click="goHome">Logo</div>
    <div class="header__caption" @click="goHome"><h1>{{$t("caption")}}</h1></div>
    <nav class="header__nav-bar">
      <ul>
        <router-link tag="li" :to="{name: 'home'}">
          <a>{{$t("navBar.home")}}</a>
        </router-link>
        <router-link tag="li" :to="{name: 'teams'}">
          <a>{{$t("navBar.teams")}}</a>
        </router-link>
        <router-link tag="li" :to="{name: 'skaters'}">
          <a>{{$t("navBar.skaters")}}</a>
        </router-link>
        <router-link tag="li" :to="{name: 'goalies'}">
          <a>{{$t("navBar.goalies")}}</a>
        </router-link>
      </ul>
    </nav>
    <div class="header__change-lang">
      <ul>
        <li @click="setLang('en')">{{$t("chooseLang.eng")}}</li>
        <li @click="setLang('ru')">{{$t("chooseLang.rus")}}</li>
      </ul>
    </div>
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
    height: 5rem;
    background: @header-color;
  }
  .header__logo {
    width: 4rem;
    height: 4rem;
    margin: 0.5rem;
    background: darkblue;
    color: @header-text-color;
    cursor: pointer;
  }
  .header__caption {
    margin-left: 1.25rem;
    font-size: 1.5rem;
    color: @header-text-color;
    cursor: pointer;
  }
  .header__nav-bar {
    margin-left: 3rem;
    ul {
      list-style-type: none;
      margin: 0;
      padding: 0;
      overflow: hidden;
      li {
        float: left;
        a {
          display: block;
          color: @header-text-color;
          text-align: center;
          padding: 1rem;
          text-decoration: none;
        &:hover {
          background-color: lightgray;
        }
        }
      }
    }
  }
  .header__change-lang {
    margin: auto 0.8rem auto auto;
    color: @header-text-color;
    font-size: 0.75rem;
    ul {
      list-style-type: none;
      margin: 0.4rem 0;
      padding: 0;
      overflow: hidden;
      text-align: right;
      li {
        cursor: pointer;
      }
    }
  }
</style>
