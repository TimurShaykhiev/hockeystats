<template>
  <header class="header container-row">
    <div class="header__logo">
    </div>
    <h1 class="header__caption">{{$t("caption")}}</h1>
    <h1 class="header__caption">{{$t("teams.NYR")}}</h1>
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
        caption: 'Hockey statistics'
      },
      ru: {
        caption: 'Хоккейная статистика'
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
    font-size: 70px;
  }
</style>
