<template>
  <div class="table-filter container-row">
    <span class="table-filter__label">{{$t("tableFilterLabel")}}</span>
    <select class="table-filter__select" v-model="selectedColumn">
      <option v-for="el in columnList" :value="el.value">{{el.name}}</option>
    </select>
    <select class="table-filter__select" v-model="selectedOperator">
      <option value="0">&gt</option>
      <option value="1">&lt</option>
      <option value="2">=</option>
    </select>
    <input type="number" class="table-filter__input" v-model="filterValue">
    <button class="table-filter__button" @click="applyFilter">{{$t("filterButtonLabel")}}</button>
    <button class="table-filter__button" @click="resetFilter">{{$t("resetButtonLabel")}}</button>
  </div>
</template>

<script>

const STAT_TIME_COLUMNS = {
  toi: true,
  toiPerGame: true
};

class FilterData {
  constructor(column, op, value) {
    this.column = column;
    this.op = op;
    this.value = value;
  }

  isEqual(data) {
    return data && this.column === data.column && this.op === data.op && this.value === data.value;
  }

  filter(stats) {
    let value = STAT_TIME_COLUMNS[this.column] ? this.value * 60 : this.value;
    let st = stats[this.column];
    if (this.op === '0') {
      return st > value;
    }
    if (this.op === '1') {
      return st < value;
    }
    return st === value;
  }
}

export default {
  name: 'table-filter',
  props: {
    columns: {type: Array, required: true}
  },
  i18n: {
    messages: {
      en: {
        tableFilterLabel: 'Filter Results By',
        filterButtonLabel: 'Apply',
        resetButtonLabel: 'Reset'
      },
      ru: {
        tableFilterLabel: 'Фильтр по',
        filterButtonLabel: 'Применить',
        resetButtonLabel: 'Сброс'
      }
    }
  },
  data() {
    return {
      selectedColumn: null,
      selectedOperator: '0',
      filterValue: ''
    };
  },
  computed: {
    columnList() {
      let result = [];
      for (let col of this.columns) {
        if (!col.hidden && col.type === 'number') {
          result.push({name: col.hint, value: col.field});
        }
      }
      return result;
    }
  },
  methods: {
    applyFilter() {
      let val = parseFloat(this.filterValue);
      if (!isNaN(val)) {
        this.$emit('apply-table-filter', new FilterData(this.selectedColumn, this.selectedOperator, val));
      }
    },

    resetFilter() {
      this.selectedColumn = null;
      this.selectedOperator = '0';
      this.filterValue = '';
      this.$emit('reset-table-filter');
    }
  }
};

</script>

<style lang="less">
  .table-filter {
    font-size: .9rem;
  }
  .table-filter__label {
    padding-top: .2rem;
  }
  .table-filter__select {
    margin-left: .8rem;
    border-radius: 4px;
  }
  .table-filter__input {
    margin-left: .8rem;
    width: 5rem;
    &::-webkit-outer-spin-button,
    &::-webkit-inner-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
  }
  .table-filter__button {
    margin-left: .8rem;
  }
</style>
