<template>
  <div
    class="alert"
    :class="{
      'alert--simple': simple,
      [`alert--${type}`]: type,
      'alert--has-icon': icon || loading,
      'alert--with-shadow': shadow,
      'alert--minimal': minimal,
    }"
  >
    <div v-if="loading" class="alert__icon">
      <div class="loading alert__icon-loading"></div>
    </div>

    <div v-if="icon && !loading" class="alert__icon">
      <i v-if="icon" :class="icon" />
    </div>

    <div>
      <div v-if="!minimal && title" class="alert__title">{{ title }}</div>

      <div class="alert__content"><slot /></div>
    </div>

    <a v-if="closeButton" class="alert__close" @click="$emit('close')">
      <i class="iconoir-cancel"></i>
    </a>
  </div>
</template>

<script>
export default {
  props: {
    type: {
      required: false,
      type: String,
      default: '',
    },
    simple: {
      required: false,
      type: Boolean,
      default: false,
    },
    shadow: {
      required: false,
      type: Boolean,
      default: false,
    },
    title: {
      required: false,
      type: String,
      default: '',
    },
    icon: {
      required: false,
      type: String,
      default: '',
    },
    loading: {
      required: false,
      type: Boolean,
      default: false,
    },
    closeButton: {
      required: false,
      type: Boolean,
      default: false,
    },
    minimal: {
      required: false,
      type: Boolean,
      default: false,
    },
  },
}
</script>
