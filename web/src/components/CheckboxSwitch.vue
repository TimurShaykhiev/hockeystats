<template>
  <div class="checkbox-switch">
    <label class="checkbox-switch__label">
      <input type="checkbox" :disabled="disabled" :checked="value" @change="$emit('input', $event.target.checked)">
      <span :class="textClasses"><slot></slot></span>
    </label>
  </div>
</template>

<script>

export default {
  name: 'checkbox-switch',
  props: {
    value: {type: Boolean, default: false},
    disabled: {type: Boolean, default: false},
    textClasses: {type: String, default: ''}
  }
};

</script>

<style lang="less">
  .checkbox-switch__label {
    input[type="checkbox"] {
      display: none;
      &:checked {
        + span {
          &:before {
            background-color: rgba(0, 127, 235, 0.5);
          }
          &:after {
            background-color: #007feb;
            transform: translate(80%, -50%);
          }
        }
      }
      + span {
        position: relative;
        display: inline-block;
        cursor: pointer;
        font-weight: 500;
        text-align: left;
        margin: 0;
        padding: 0 44px;
        &:before,
        &:after {
          content: '';
          cursor: pointer;
          position: absolute;
          margin: 0;
          outline: 0;
          top: 50%;
          transform: translate(0, -50%);
          transition: all 200ms ease-out;
        }
        &:before {
          left: 1px;
          width: 34px;
          height: 14px;
          background-color: rgba(0, 0, 0, 0.2);
          border-radius: 8px;
        }
        &:after {
          left: 0;
          width: 20px;
          height: 20px;
          background-color: rgba(0, 0, 0, 0.5);
          border-radius: 50%;
          box-shadow: 0 3px 1px -2px rgba(0, 0, 0, .14), 0 2px 2px 0 rgba(0, 0, 0, .098), 0 1px 5px 0 rgba(0, 0, 0, .084);
        }
      }
      &:checked + span &:after {
        transform: translate(80%, -50%);
      }
    }
  }
</style>
