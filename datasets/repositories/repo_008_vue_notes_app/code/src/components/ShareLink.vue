<template>
  <div class="share-link">
    <input readonly :value="link" />
    <button type="button" @click="copy">Copy</button>
  </div>
</template>

<script>
export default {
  props: { noteId: { type: [String, Number], required: true } },
  computed: {
    link() {
      return `${window.location.origin}/notes/${this.noteId}`;
    },
  },
  methods: {
    copy() {
      navigator.clipboard.writeText(this.link);
    },
  },
};
</script>
