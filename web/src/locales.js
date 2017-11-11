import Vue from 'vue';
import VueI18n from 'vue-i18n';
import UserSettings from 'Root/userSettings';

Vue.use(VueI18n);

let locales = {
  locale: 'en',
  fallbackLocale: 'en',
  silentTranslationWarn: true,
  messages: {
    en: {
      teams: {
        1: 'New Jersey Devils',
        2: 'New York Islanders',
        3: 'New York Rangers',
        4: 'Philadelphia Flyers',
        5: 'Pittsburgh Penguins',
        6: 'Boston Bruins',
        7: 'Buffalo Sabres',
        8: 'Montréal Canadiens',
        9: 'Ottawa Senators',
        10: 'Toronto Maple Leafs',
        12: 'Carolina Hurricanes',
        13: 'Florida Panthers',
        14: 'Tampa Bay Lightning',
        15: 'Washington Capitals',
        16: 'Chicago Blackhawks',
        17: 'Detroit Red Wings',
        18: 'Nashville Predators',
        19: 'St. Louis Blues',
        20: 'Calgary Flames',
        21: 'Colorado Avalanche',
        22: 'Edmonton Oilers',
        23: 'Vancouver Canucks',
        24: 'Anaheim Ducks',
        25: 'Dallas Stars',
        26: 'Los Angeles Kings',
        28: 'San Jose Sharks',
        29: 'Columbus Blue Jackets',
        30: 'Minnesota Wild',
        52: 'Winnipeg Jets',
        53: 'Arizona Coyotes',
        54: 'Vegas Golden Knights'
      },
      conferences: {
        5: 'Western conference',
        6: 'Eastern conference'
      }
    },
    ru: {
      teams: {
        1: 'Нью-Джерси Дэвилс',
        2: 'Нью-Йорк Айлендерс',
        3: 'Нью-Йорк Рейнджерс',
        4: 'Филадельфия Флайерз',
        5: 'Питтсбург Пингвинз',
        6: 'Бостон Брюинз',
        7: 'Баффало Сэйбрз',
        8: 'Монреаль Канадиенс',
        9: 'Оттава Сенаторз',
        10: 'Торонто Мэйпл Лифс',
        12: 'Каролина Харрикейнз',
        13: 'Флорида Пантерз',
        14: 'Тампа-Бэй Лайтнинг',
        15: 'Вашингтон Кэпиталз',
        16: 'Чикаго Блэкхоукс',
        17: 'Детройт Ред Уингз',
        18: 'Нэшвилл Предаторз',
        19: 'Сент-Луис Блюз',
        20: 'Калгари Флэймз',
        21: 'Колорадо Эвеланш',
        22: 'Эдмонтон Ойлерз',
        23: 'Ванкувер Кэнакс',
        24: 'Анахайм Дакс',
        25: 'Даллас Старз',
        26: 'Лос-Анджелес Кингз',
        28: 'Сан-Хосе Шаркс',
        29: 'Коламбус Блю Джекетс',
        30: 'Миннесота Уайлд',
        52: 'Виннипег Джетс',
        53: 'Аризона Койотс',
        54: 'Вегас Голден Найтс'
      },
      conferences: {
        5: 'Западная конференция',
        6: 'Восточная конференция'
      }
    }
  }
};

const settings = new UserSettings();
locales.locale = settings.locale;

export default new VueI18n(locales);
