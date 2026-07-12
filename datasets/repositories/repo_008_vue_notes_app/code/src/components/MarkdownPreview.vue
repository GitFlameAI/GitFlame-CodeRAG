<template>
  <div class="markdown-preview" v-html="rendered"></div>
</template>

<script>
export default {
  props: { source: { type: String, default: "" } },
  computed: {
    rendered() {
      return this.source
        .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*(.+?)\*/g, "<em>$1</em>")
        .replace(/\n/g, "<br />");
    },
  },
};
</script>
