<template>
  <div class="tabs-component">
    <ul class="tabs-component__tabs">
      <li v-for="(tab, i) in tabs" :key="i"
        :class="{'is-active': tab.isActive, 'is-disabled': tab.isDisabled}"
        class="tabs-component__tab">
        <a v-html="tab.header" href=""
           @click="selectTab(tab.id, $event)"
           class="tabs-component__tab-a"></a>
      </li>
    </ul>
    <div class="tabs-component__panels">
      <slot/>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      tabs: []
    };
  },
  created() {
    this.tabs = this.$children;
  },
  mounted() {
    if (this.tabs.length) {
      this.selectTab(this.tabs[0].id);
    }
  },
  methods: {
    findTab(tabId) {
      return this.tabs.find((tab) => tab.id === tabId);
    },

    selectTab(selectedTabId, event) {
      if (event) {
        event.preventDefault();
      }
      const selectedTab = this.findTab(selectedTabId);
      if (!selectedTab || selectedTab.isDisabled) {
        return;
      }
      this.tabs.forEach((tab) => {
        tab.isActive = (tab.id === selectedTab.id);
      });
    }
  }
};

</script>

<style lang="less">
  @import '../../styles/vars.less';

  .tabs-component {
    margin: 2rem 0;
  }

  .tabs-component__tabs {
    border: solid 1px @border-color;
    border-radius: 6px;
    margin-bottom: .3rem;

    @media (min-width: 700px) {
      border: 0;
      align-items: stretch;
      display: flex;
      justify-content: flex-start;
      margin-bottom: -1px;
    }
  }

  .tabs-component__tab {
    color: @text-color-faded;
    font-size: .9rem;
    font-weight: 600;
    margin-right: 0;
    list-style: none;

    &:not(:last-child) {
      border-bottom: dotted 1px @border-color;
    }
    &:hover {
      color: @text-color-faded-hover;
    }
    &.is-active {
      color: #000;
    }
    &.is-disabled * {
      color: @text-color-disabled;
      cursor: not-allowed !important;
    }
    @media (min-width: 700px) {
      background-color: @general-background-color;
      border: solid 1px @border-color;
      border-radius: 3px 3px 0 0;
      margin-right: .5rem;
      transform: translateY(2px);
      transition: transform .3s ease;

      &.is-active {
        border-bottom: solid 1px @general-background-color;
        z-index: 2;
        transform: translateY(0);
      }
    }
  }

  .tabs-component__tab-a {
    align-items: center;
    color: inherit;
    display: flex;
    padding: .75rem 1rem;
    text-decoration: none;
  }

  .tabs-component__panels {
    padding: 2rem 0;
    position: relative;

    @media (min-width: 700px) {
      background-color: @general-background-color;
      border: solid 1px @border-color;
      border-radius: 0 6px 6px 6px;
      box-shadow: 0 0 10px rgba(0, 0, 0, .05);
      padding: 2rem;
    }
  }
</style>
