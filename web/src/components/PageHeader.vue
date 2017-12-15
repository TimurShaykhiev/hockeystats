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
  @textColor: white;

  .header {
    align-items: center;
    height: 80px;
    background: blue;
  }
  .header__logo {
    width: 60px;
    height: 60px;
    margin: 5px;
    background: darkblue;
    color: @textColor;
    cursor: pointer;
  }
  .header__caption {
    margin-left: 20px;
    font-size: 24px;
    color: @textColor;
    cursor: pointer;
  }
  .header__nav-bar {
    margin-left: 50px;
    ul {
      list-style-type: none;
      margin: 0;
      padding: 0;
      overflow: hidden;
      li {
        float: left;
        a {
          display: block;
          color: @textColor;
          text-align: center;
          padding: 16px;
          text-decoration: none;
        &:hover {
          background-color: lightgray;
        }
        }
      }
    }
  }
  .header__change-lang {
    margin: auto 10px auto auto;
    color: @textColor;
    font-size: 12px;
    ul {
      list-style-type: none;
      margin: 5px 0;
      padding: 0;
      overflow: hidden;
      text-align: right;
      li {
        cursor: pointer;
      }
    }
  }
</style>
