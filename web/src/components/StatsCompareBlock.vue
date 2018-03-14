<template>
  <div class="stats-compare-block">
    <table>
      <tr>
        <th class="compare-block--left">{{caption.lName}}</th>
        <th class="stats-compare-block__title">{{caption.title}}</th>
        <th class="compare-block--right">{{caption.rName}}</th>
      </tr>
      <tr v-for="el in stats">
        <td class="number-cell" :class="{'compare-block--left': el.leftColor}">{{el.lValue}}</td>
        <td class="name-cell">{{el.name}}</td>
        <td class="number-cell" :class="{'compare-block--right': el.rightColor}">{{el.rValue}}</td>
      </tr>
    </table>
  </div>
</template>

<script>

export default {
  name: 'stats-compare-block',
  props: {
    caption: {required: true},
    items: {required: true}
  },
  computed: {
    stats() {
      return this.items.map((el) => {
        let left = false;
        let right = false;
        const diff = el.lValue.value - el.rValue.value;
        if (diff !== 0) {
          if (el.sortOrder === 'desc') {
            left = diff > 0;
          } else {
            left = diff < 0;
          }
          right = !left;
        }
        return {
          name: el.name,
          lValue: el.lValue.toStr(),
          rValue: el.rValue.toStr(),
          leftColor: left,
          rightColor: right
        };
      });
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .stats-compare-block {
    table {
      border-collapse: collapse;
      border: 1px solid @border-color;
      margin: 1rem;
    }
    tr {
      height: 2rem;
    }
    th {
      border: 1px solid @border-color;

      &.stats-compare-block__title {
        color: #fff;
        background-color: @compare-caption-color;
      }
    }
    td {
      border: 1px solid @border-color;
      text-align: center;

      &.name-cell {
        width: 13rem;
      }
      &.number-cell {
        min-width: 4rem;
      }
      &.stats-compare-block__title {
        color: #fff;
        background-color: @compare-caption-color;
      }
    }
  }
</style>
