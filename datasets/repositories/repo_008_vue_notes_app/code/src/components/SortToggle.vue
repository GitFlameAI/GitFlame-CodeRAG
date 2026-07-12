<template>
  <button type="button" class="sort-toggle" @click="toggle">
    Sort: {{ ascending ? "Oldest first" : "Newest first" }}
  </button>
</template>

<script>
export default {
  props: { ascending: { type: Boolean, default: true } },
  emits: ["update:ascending"],
  methods: {
    toggle() {
      this.$emit("update:ascending", !this.ascending);
    },
  },
};
</script>
