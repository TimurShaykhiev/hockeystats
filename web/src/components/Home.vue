<template>
  <div class="home">
    <h2 class="home__season-name">{{seasonName}}</h2>
    <div class="home__leader-preview-container container-row">
      <leaders-preview type="skaterGoal"></leaders-preview>
      <leaders-preview type="skaterAssist"></leaders-preview>
      <leaders-preview type="skaterPoint"></leaders-preview>
      <leaders-preview type="skaterPlusMinus"></leaders-preview>
      <leaders-preview type="goalieGaa"></leaders-preview>
      <leaders-preview type="goalieSavePercentage"></leaders-preview>
    </div>
    <div class="home__standings-container">
      <h2 class="home__standings-title">{{$t('home.title')}}</h2>
      <tabs>
        <tab :name="$t('home.tabNames.divisions')">
          <div class="home__standings-conf-div container-col">
            <h3 class="home__conf-name">{{conference1}}</h3>
            <div class="home__standings-div container-row">
              <standings type="div" :confSerialNum="1" :divSerialNum="1"/>
              <standings type="div" :confSerialNum="1" :divSerialNum="2"/>
            </div>
            <h3 class="home__conf-name">{{conference2}}</h3>
            <div class="home__standings-div container-row">
              <standings type="div" :confSerialNum="2" :divSerialNum="1"/>
              <standings type="div" :confSerialNum="2" :divSerialNum="2"/>
            </div>
          </div>
        </tab>
        <tab :name="$t('home.tabNames.conferences')">
          <div class="home__standings-conf container-row">
            <standings type="conf" :confSerialNum="1"/>
            <standings type="conf" :confSerialNum="2"/>
          </div>
        </tab>
        <tab :name="$t('home.tabNames.wildCards')">
          <div class="home__standings-conf-wc container-row">
            <div class="home__standings-wc container-col">
              <h3 class="home__conf-name">{{conference1}}</h3>
              <standings type="wc" :confSerialNum="1" :divSerialNum="1"/>
              <standings type="wc" :confSerialNum="1" :divSerialNum="2"/>
              <standings type="wc" :confSerialNum="1"/>
            </div>
            <div class="home__standings-wc container-col">
              <h3 class="home__conf-name">{{conference2}}</h3>
              <standings type="wc" :confSerialNum="2" :divSerialNum="1"/>
              <standings type="wc" :confSerialNum="2" :divSerialNum="2"/>
              <standings type="wc" :confSerialNum="2"/>
            </div>
            </div>
        </tab>
        <tab :name="$t('home.tabNames.league')">
          <div class="home__standings-league container-row">
            <standings type="league"/>
          </div>
        </tab>
        <tab :name="$t('home.tabNames.playOff')">
          <play-off/>
        </tab>
      </tabs>
    </div>
  </div>
</template>

<script>
import LeadersPreview from 'Components/LeadersPreview';
import Standings from 'Components/Standings';
import PlayOff from 'Components/PlayOff';
import CompUtils from 'Components/utils';

export default {
  name: 'home',
  components: {LeadersPreview, Standings, PlayOff},
  i18n: {
    messages: {
      en: {
        home: {
          title: 'Standings',
          tabNames: {
            divisions: 'Divisions',
            conferences: 'Conferences',
            wildCards: 'Wild Cards',
            league: 'League',
            playOff: 'Playoff'
          }
        }
      },
      ru: {
        home: {
          title: 'Турнирная таблица',
          tabNames: {
            divisions: 'Дивизионы',
            conferences: 'Конференции',
            wildCards: 'Уайлд карды',
            league: 'Лига',
            playOff: 'Плей-офф'
          }
        }
      }
    }
  },
  computed: {
    seasonName() {
      let season = this.$store.state.season.currentSeason;
      if (season.id !== undefined) {
        return CompUtils.seasonToStr(season);
      }
      return '';
    },

    conference1() {
      let conf = this.$store.getters.getConferenceBySerialNumber(1);
      return conf !== null ? conf.name : '';
    },

    conference2() {
      let conf = this.$store.getters.getConferenceBySerialNumber(2);
      return conf !== null ? conf.name : '';
    }
  }
};

</script>

<style lang="less">
  .home__season-name {
    text-align: center;
    margin: 1rem 0;
  }
  .home__leader-preview-container {
    justify-content: space-evenly;
  }
  .home__standings-container {
    width: 100%;
    margin-top: 2rem;
  }
  .home__standings-title {
    font-size: 2rem;
  }
  .home__conf-name {
    font-size: 1.8rem;
    width: 100%;
    text-align: center;
    margin: 1rem 0;
  }
  .home__standings-conf {
    justify-content: space-around;
  }
  .home__standings-div {
    justify-content: space-around;
  }
  .home__standings-conf-wc {
    justify-content: space-around;
  }
  .home__standings-league {
    justify-content: center;
  }
</style>
