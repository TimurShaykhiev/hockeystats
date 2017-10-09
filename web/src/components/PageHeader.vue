<template>
  <header class="header container-row">
    <div class="header__logo">Logo</div>
    <div class="header__caption">{{$t("caption")}}</div>
    <nav class="header__nav-bar">
      <ul>
        <router-link tag="li" :to="{name: 'home'}">
          <a>{{$t("navBar.home")}}</a>
        </router-link>
        <router-link tag="li" :to="{name: 'teams'}">
          <a>{{$t("navBar.teams")}}</a>
        </router-link>
        <router-link tag="li" :to="{name: 'players'}">
          <a>{{$t("navBar.players")}}</a>
        </router-link>
      </ul>
    </nav>
    <button @click="changeLang">Change lang</button>
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
          players: 'Players'
        }
      },
      ru: {
        caption: 'Хоккейная статистика',
        navBar: {
          home: 'Главная',
          teams: 'Команды',
          players: 'Игроки'
        }
      }
    }
  },
  methods: {
    changeLang() {
      const settings = new UserSettings();
      settings.locale = settings.locale === 'en' ? 'ru' : 'en';
      location.reload();
    }
  }
};

</script>

<style lang="less">
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
    color: white;
  }
  .header__caption {
    margin-left: 20px;
    font-size: 34px;
    color: white;
  }
  .header__nav-bar {
    ul {
      list-style-type: none;
      margin: 0;
      padding: 0;
      overflow: hidden;
      li {
        float: left;
        a {
          display: block;
          color: white;
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
</style>
