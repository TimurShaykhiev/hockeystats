import Vue from 'vue';
import VueI18n from 'vue-i18n';
import UserSettings from 'Root/userSettings';

Vue.use(VueI18n);

let locales = {
  locale: 'ru',
  fallbackLocale: 'ru',
  silentTranslationWarn: true,
  messages: {
    en: {
      statNames: {
        season: 'Season',
        seasonShort: 'Season',
        team: 'Team',
        teamShort: 'Team',
        games: 'Games Played',
        gamesShort: 'GP',
        winRegular: 'Wins Regular',
        winRegularShort: 'WR',
        winOvertime: 'Wins Overtime',
        winOvertimeShort: 'WO',
        winShootout: 'Wins Shootout',
        winShootoutShort: 'WS',
        loseRegular: 'Losses Regular',
        loseRegularShort: 'LR',
        loseOvertime: 'Losses Overtime',
        loseOvertimeShort: 'LO',
        loseShootout: 'Losses Shootout',
        loseShootoutShort: 'LS',
        points: 'Points',
        pointsShort: 'P',
        pointPercentage: 'Points Percentage',
        pointPercentageShort: 'P%',
        goalsFor: 'Goals For',
        goalsForShort: 'GF',
        goalsAgainst: 'Goals Against',
        goalsAgainstShort: 'GA',
        shots: 'Shots',
        shotsShort: 'Shots',
        ppPercentage: 'Power Play Percentage',
        ppPercentageShort: 'PP%',
        pkPercentage: 'Penalty Kill Percentage',
        pkPercentageShort: 'PK%',
        faceOffWinsPercentage: 'Faceoff Win Percentage',
        faceOffWinsPercentageShort: 'FOW%',
        goalsForPerGame: 'Goals For Per Game',
        goalsForPerGameShort: 'GF/GP',
        goalsAgainstPerGame: 'Goals Against Per Game',
        goalsAgainstPerGameShort: 'GA/GP',
        shotsPerGame: 'Shots Per Game',
        shotsPerGameShort: 'Sh/GP',
        blocks: 'Blocks',
        blocksShort: 'BL',
        takeaways: 'Takeaways',
        takeawaysShort: 'TAw',
        giveaways: 'Giveaways',
        giveawaysShort: 'GAw',
        hits: 'Hits',
        hitsShort: 'Hits',
        penaltyMinutes: 'Penalty Minutes',
        penaltyMinutesShort: 'PIM',
        goals: 'Goals',
        goalsShort: 'G',
        assists: 'Assists',
        assistsShort: 'A',
        plusMinus: 'Plus-Minus',
        plusMinusShort: '+/-',
        pointsPerGame: 'Points Per Game',
        pointsPerGameShort: 'P/GP',
        powerPlay: 'Power Play',
        powerPlayShort: 'PP',
        ppGoals: 'Power Play Goals',
        ppGoalsShort: 'PPG',
        ppPoints: 'Power Play Points',
        ppPointsShort: 'PPP',
        ppAssists: 'Power Play Assists',
        shGoals: 'Shorthanded Goals',
        shGoalsShort: 'SHG',
        shPoints: 'Shorthanded Points',
        shPointsShort: 'SHP',
        shAssists: 'Shorthanded Assists',
        evenGoals: 'Even Strength Goals',
        evenPoints: 'Even Strength Points',
        evenAssists: 'Even Strength Assists',
        shootingPercentage: 'Shooting Percentage',
        shootingPercentageShort: 'S%',
        toiPerGame: 'Time On Ice Per Game',
        toiPerGameShort: 'TOI/GP',
        wins: 'Wins',
        winsShort: 'W',
        losses: 'Losses',
        lossesShort: 'L',
        shotsAgainst: 'Shots Against',
        shotsAgainstShort: 'SA',
        saves: 'Saves',
        savesShort: 'Svs',
        savePercentage: 'Save Percentage',
        savePercentageShort: 'Sv%',
        goalsAgainstAverage: 'Goals Against Average',
        goalsAgainstAverageShort: 'GAA',
        shutouts: 'Shutouts',
        shutoutsShort: 'SO',
        timeOnIce: 'Time On Ice',
        timeOnIceShort: 'TOI',
        shotsAgainstPerGame: 'Shots Against Per Game',
        oppShootingPercentage: 'Opponent Shooting Percentage',
        scoringEfficiencyRatio: 'Scoring Efficiency Ratio',
        shotEfficiencyRatio: 'Shot Efficiency Ratio',
        penaltyEfficiencyRatio: 'Penalty Efficiency Ratio',
        ppGoalsPerGame: 'Power Play Goals Per Game',
        ppPerGame: 'Power Plays Per Game',
        shGoalsAgainst: 'Short Handed Goals Against',
        shGoalsAgainstPerGame: 'Short Handed Goals Against Per Game',
        shPerGame: 'Penalty Kills Per Game',
        oppSavePercentage: 'Opponent Save Percentage',
        winPercentage: 'Win Percentage',
        savesPerGame: 'Saves Per Game',
        shotsAgainstPerGoal: 'Shots Against Per Goal',
        evenStrengthGoalsAgainst: 'Even Strength Goals Against',
        evenStrengthGoalsAgainstPercentage: 'Even Strength Goals Against %',
        ppGoalsAllowed: 'Power Play Goals Allowed',
        shGoalsAllowed: 'Short Handed Goals Allowed',
        turnover: 'Turnover +/-',
        pointsPer60min: 'Points Per 60 min',
        goalPercentageOfPoints: 'Goal Percentage of Points',
        assistPercentageOfPoints: 'Assist Percentage of Points',
        goalsPerGame: 'Goals Per Game',
        goalsPer60min: 'Goals Per 60 min',
        evenStrengthGoalsPercentage: 'Even Strength Goal Percentage',
        ppGoalPercentage: 'Power Play Goal Percentage',
        assistsPerGame: 'Assists Per Game',
        assistsPer60min: 'Assists Per 60 min',
        evenAssistPercentage: 'Even Strength Assist Percentage',
        ppAssistPercentage: 'Power Play Assist Percentage',
        shotsPer60min: 'Shots Per 60 min',
        shotsPerGoal: 'Shots Per Goal',
        turnoverPer60min: 'Turnover +/- Per 60 min',
        turnoverRatio: 'Turnover Ratio',
        blocksPer60min: 'Blocks Per 60 min',
        hitsPer60min: 'Hits Per 60 min',
        PIMsPer60min: 'PIM Per 60 min',
        homeWinPercentage: 'Home Win Percentage',
        awayWinPercentage: 'Away Win Percentage',
        shootoutWinPercentage: 'Shootout Win Percentage',
        oppShutouts: 'Opponent shutouts'
      },
      season: {
        regular: 'Regular season',
        playoff: 'Playoff'
      },
      playerPosition: {
        C: 'C',
        R: 'R',
        L: 'L',
        D: 'D',
        G: 'G'
      },
      pagination: {
        next: 'Next',
        prev: 'Prev',
        rowsPerPage: 'Rows Per Page',
        ofText: 'of',
        allText: 'All'
      },
      ordinalNumbers: ['TH', 'ST', 'ND', 'RD', 'TH', 'TH', 'TH', 'TH', 'TH', 'TH'],
      tabNames: {
        table: 'Table',
        charts: 'Charts'
      },
      charts: {
        points: 'Points',
        goalsAssists: 'Goals & Assists',
        goals: 'Goals',
        assists: 'Assists',
        toi: 'Time On Ice',
        toiCaptionY: 'Minutes',
        skaterSkills: 'Skater Skills',
        plusMinus: 'Plus-Minus',
        pointsPerGame: 'Points Per Game',
        savePercentage: 'Save Percentage',
        goalsAgainstAverage: 'Goals Against Average',
        wins: 'Wins',
        shutouts: 'Shutouts',
        losses: 'Losses',
        teamSkills: 'Team Skills',
        ppPercentage: 'Power Play Percentage',
        pkPercentage: 'Penalty Kill Percentage',
        penaltyMinutes: 'Penalty Minutes',
        games: 'Games',
        homeAway: 'Home/Away Skills',
        homeGames: 'Home Games',
        awayGames: 'Away Games',
        goalsFor: 'Goals For',
        goalsAgainst: 'Goals Against',
        goalsDiff: 'Goals Difference',
        pointsProgress: 'Points Progress',
        faceoffWin: 'Faceoff Win'
      },
      itemSelectorPlaceholder: {
        team: 'Select a team',
        skater: 'Select a skater',
        goalie: 'Select a goaltender'
      }
    },
    ru: {
      statNames: {
        season: 'Сезон',
        seasonShort: 'Сезон',
        team: 'Команда',
        teamShort: 'Команда',
        games: 'Сыграно матчей',
        gamesShort: 'М',
        winRegular: 'Выигрыши в основное время',
        winRegularShort: 'В',
        winOvertime: 'Выигрыши в доп. время',
        winOvertimeShort: 'ВО',
        winShootout: 'Выигрыши по буллитам',
        winShootoutShort: 'ВБ',
        loseRegular: 'Поражения в основное время',
        loseRegularShort: 'П',
        loseOvertime: 'Поражения в доп. время',
        loseOvertimeShort: 'ПО',
        loseShootout: 'Поражения по буллитам',
        loseShootoutShort: 'ПБ',
        points: 'Очки',
        pointsShort: 'О',
        pointPercentage: 'Процент набранных очков',
        pointPercentageShort: '%О',
        goalsFor: 'Заброшенные шайбы',
        goalsForShort: 'Ш',
        goalsAgainst: 'Пропущенные шайбы',
        goalsAgainstShort: 'ПШ',
        shots: 'Броски в створ',
        shotsShort: 'Бр',
        ppPercentage: 'Процент реализации большинства',
        ppPercentageShort: '%БОЛ',
        pkPercentage: 'Процент нейтрализации меньшинства',
        pkPercentageShort: '%МЕН',
        faceOffWinsPercentage: 'Процент выигранных вбрасываний',
        faceOffWinsPercentageShort: '%Вбр',
        goalsForPerGame: 'В среднем заброшенных шайб за матч',
        goalsForPerGameShort: 'ЗШ/М',
        goalsAgainstPerGame: 'В среднем пропущенных шайб за матч',
        goalsAgainstPerGameShort: 'ПШ/М',
        shotsPerGame: 'В среднем бросков в створ за матч',
        shotsPerGameShort: 'Бр/М',
        blocks: 'Блокированные броски',
        blocksShort: 'Бл',
        takeaways: 'Отборы шайбы',
        takeawaysShort: 'ОтбШ',
        giveaways: 'Потери шайбы',
        giveawaysShort: 'ПотШ',
        hits: 'Силовые приёмы',
        hitsShort: 'Сил',
        penaltyMinutes: 'Минуты штрафа',
        penaltyMinutesShort: 'Штр',
        goals: 'Голы',
        goalsShort: 'Г',
        assists: 'Пасы',
        assistsShort: 'П',
        plusMinus: 'Плюс-минус',
        plusMinusShort: '+/-',
        pointsPerGame: 'В среднем очков за матч',
        pointsPerGameShort: 'Г/М',
        powerPlay: 'Большинство',
        powerPlayShort: 'БОЛ',
        ppGoals: 'Голы в большинстве',
        ppGoalsShort: 'Г БОЛ',
        ppPoints: 'Очки в большинстве',
        ppPointsShort: 'О БОЛ',
        ppAssists: 'Пасы в большинстве',
        shGoals: 'Голы в меньшинстве',
        shGoalsShort: 'Г МЕН',
        shPoints: 'Очки в меньшинстве',
        shPointsShort: 'О МЕН',
        shAssists: 'Пасы в меньшинстве',
        evenGoals: 'Голы в равных составах',
        evenPoints: 'Очки в равных составах',
        evenAssists: 'Пасы в равных составах',
        shootingPercentage: 'Процент реализации бросков',
        shootingPercentageShort: '%Бр',
        toiPerGame: 'Время на льду за матч',
        toiPerGameShort: 'ВРМ/М',
        wins: 'Выигрыши',
        winsShort: 'В',
        losses: 'Поражения',
        lossesShort: 'П',
        shotsAgainst: 'Броски по своим воротам',
        shotsAgainstShort: 'Бр',
        saves: 'Спасения',
        savesShort: 'Сп',
        savePercentage: 'Процент отраженных бросков',
        savePercentageShort: '%ОБ',
        goalsAgainstAverage: 'Коэффициент надёжности',
        goalsAgainstAverageShort: 'КН',
        shutouts: 'Матчи на ноль',
        shutoutsShort: 'СМ',
        timeOnIce: 'Время на льду',
        timeOnIceShort: 'ВРМ',
        shotsAgainstPerGame: 'В среднем бросков по своим воротам за матч',
        oppShootingPercentage: 'Процент реализации бросков противника',
        scoringEfficiencyRatio: 'Отношение забитых/пропущенных голов',
        shotEfficiencyRatio: 'Отношение своих/чужих бросков',
        penaltyEfficiencyRatio: 'Отношение чужих/своих штрафных минут',
        ppGoalsPerGame: 'Голов в большинстве в среднем за матч',
        ppPerGame: 'Розыгрышей большинства в среднем за матч',
        shGoalsAgainst: 'Пропущенные голы в меньшинстве',
        shGoalsAgainstPerGame: 'Пропущенных голов в меньшинстве в среднем за матч',
        shPerGame: 'Розыгрышей меньшинства в среднем за матч',
        oppSavePercentage: 'Процент отраженных бросков противника',
        winPercentage: 'Процент побед',
        savesPerGame: 'Спасений в среднем за матч',
        shotsAgainstPerGoal: 'В среднем бросков по своим воротам на гол',
        evenStrengthGoalsAgainst: 'Пропущенные голы в равных составах',
        evenStrengthGoalsAgainstPercentage: 'Процент пропущенных голов в равных составах',
        ppGoalsAllowed: 'Пропущенные голы в меньшинстве',
        shGoalsAllowed: 'Пропущенные голы в большинстве',
        turnover: 'Отборы и потери шайбы +/-',
        pointsPer60min: 'Очки за 60 мин',
        goalPercentageOfPoints: 'Процент голов от набранных очков',
        assistPercentageOfPoints: 'Процент пасов от набранных очков',
        goalsPerGame: 'Голов в среднем за матч',
        goalsPer60min: 'Голы за 60 мин',
        evenStrengthGoalsPercentage: 'Процент голов в равных составах',
        ppGoalPercentage: 'Процент голов в большинстве',
        assistsPerGame: 'Пасов в среднем за матч',
        assistsPer60min: 'Пасы за 60 мин',
        evenAssistPercentage: 'Процент пасов в равных составах',
        ppAssistPercentage: 'Процент пасов в большинстве',
        shotsPer60min: 'Броски за 60 мин',
        shotsPerGoal: 'Бросков на гол',
        turnoverPer60min: 'Отборы и потери шайбы +/- за 60 мин',
        turnoverRatio: 'Отношение отборов/потерь шайбы',
        blocksPer60min: 'Блокированные броски за 60 мин',
        hitsPer60min: 'Силовые приёмы за 60 мин',
        PIMsPer60min: 'Штрафные минуты за 60 мин',
        homeWinPercentage: 'Процент домашних побед',
        awayWinPercentage: 'Процент гостевых побед',
        shootoutWinPercentage: 'Процент побед по буллитам',
        oppShutouts: 'Матчи на ноль у противника'
      },
      season: {
        regular: 'Регулярный сезон',
        playoff: 'Плей-офф'
      },
      playerPosition: {
        C: 'ЦН',
        R: 'ПН',
        L: 'ЛН',
        D: 'Защ',
        G: 'Вр'
      },
      pagination: {
        next: 'След',
        prev: 'Пред',
        rowsPerPage: 'Строк на стр.',
        ofText: 'из',
        allText: 'Все'
      },
      ordinalNumbers: ['й', 'й', 'й', 'й', 'й', 'й', 'й', 'й', 'й', 'й'],
      tabNames: {
        table: 'Таблица',
        charts: 'Графики'
      },
      charts: {
        points: 'Очки',
        goalsAssists: 'Голы и пасы',
        goals: 'Голы',
        assists: 'Пасы',
        toi: 'Время на льду',
        toiCaptionY: 'Минуты',
        skaterSkills: 'Основные навыки',
        plusMinus: 'Плюс-минус',
        pointsPerGame: 'В среднем очков за матч',
        savePercentage: 'Процент отраженных бросков',
        goalsAgainstAverage: 'Коэффициент надёжности',
        wins: 'Победы',
        shutouts: 'Матчи на ноль',
        losses: 'Поражения',
        teamSkills: 'Основные показатели',
        ppPercentage: 'Процент реализации большинства',
        pkPercentage: 'Процент нейтрализации меньшинства',
        penaltyMinutes: 'Минуты штрафа',
        games: 'Игры',
        homeAway: 'Домашние/Гостевые показатели',
        homeGames: 'Домашние игры',
        awayGames: 'Гостевые игры',
        goalsFor: 'Заброшенные шайбы',
        goalsAgainst: 'Пропущенные шайбы',
        goalsDiff: 'Разница шайб',
        pointsProgress: 'Набор очков',
        faceoffWin: 'Выигранные вбрасывания'
      },
      itemSelectorPlaceholder: {
        team: 'Выбери команду',
        skater: 'Выбери игрока',
        goalie: 'Выбери вратаря'
      }
    }
  }
};

const settings = new UserSettings();
locales.locale = settings.locale;

export default new VueI18n(locales);
