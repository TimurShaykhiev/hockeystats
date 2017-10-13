import Vue from 'vue';
import VueI18n from 'vue-i18n';
import UserSettings from 'Root/userSettings';

Vue.use(VueI18n);

let locales = {
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en: {
      teams: {
        'NJD': 'New Jersey Devils',
        'NYI': 'New York Islanders',
        'NYR': 'New York Rangers',
        'PHI': 'Philadelphia Flyers',
        'PIT': 'Pittsburgh Penguins',
        'BOS': 'Boston Bruins',
        'BUF': 'Buffalo Sabres',
        'MTL': 'Montréal Canadiens',
        'OTT': 'Ottawa Senators',
        'TOR': 'Toronto Maple Leafs',
        'CAR': 'Carolina Hurricanes',
        'FLA': 'Florida Panthers',
        'TBL': 'Tampa Bay Lightning',
        'WSH': 'Washington Capitals',
        'CHI': 'Chicago Blackhawks',
        'DET': 'Detroit Red Wings',
        'NSH': 'Nashville Predators',
        'STL': 'St. Louis Blues',
        'CGY': 'Calgary Flames',
        'COL': 'Colorado Avalanche',
        'EDM': 'Edmonton Oilers',
        'VAN': 'Vancouver Canucks',
        'ANA': 'Anaheim Ducks',
        'DAL': 'Dallas Stars',
        'LAK': 'Los Angeles Kings',
        'SJS': 'San Jose Sharks',
        'CBJ': 'Columbus Blue Jackets',
        'MIN': 'Minnesota Wild',
        'WPG': 'Winnipeg Jets',
        'ARI': 'Arizona Coyotes',
        'VGK': 'Vegas Golden Knights'
      }
    },
    ru: {
      teams: {
        'NJD': 'Нью-Джерси Дэвилс',
        'NYI': 'Нью-Йорк Айлендерс',
        'NYR': 'Нью-Йорк Рейнджерс',
        'PHI': 'Филадельфия Флайерз',
        'PIT': 'Питтсбург Пингвинз',
        'BOS': 'Бостон Брюинз',
        'BUF': 'Баффало Сэйбрз',
        'MTL': 'Монреаль Канадиенс',
        'OTT': 'Оттава Сенаторз',
        'TOR': 'Торонто Мэйпл Лифс',
        'CAR': 'Каролина Харрикейнз',
        'FLA': 'Флорида Пантерз',
        'TBL': 'Тампа-Бэй Лайтнинг',
        'WSH': 'Вашингтон Кэпиталз',
        'CHI': 'Чикаго Блэкхоукс',
        'DET': 'Детройт Ред Уингз',
        'NSH': 'Нэшвилл Предаторз',
        'STL': 'Сент-Луис Блюз',
        'CGY': 'Калгари Флэймз',
        'COL': 'Колорадо Эвеланш',
        'EDM': 'Эдмонтон Ойлерз',
        'VAN': 'Ванкувер Кэнакс',
        'ANA': 'Анахайм Дакс',
        'DAL': 'Даллас Старз',
        'LAK': 'Лос-Анджелес Кингз',
        'SJS': 'Сан-Хосе Шаркс',
        'CBJ': 'Коламбус Блю Джекетс',
        'MIN': 'Миннесота Уайлд',
        'WPG': 'Виннипег Джетс',
        'ARI': 'Аризона Койотс',
        'VGK': 'Вегас Голден Найтс'
      }
    }
  }
};

const settings = new UserSettings();
locales.locale = settings.locale;

export default new VueI18n(locales);
