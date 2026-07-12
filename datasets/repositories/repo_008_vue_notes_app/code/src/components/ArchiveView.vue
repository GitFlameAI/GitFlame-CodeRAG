<template>
  <ul class="archive-view">
    <li v-for="note in archivedNotes" :key="note.id">
      <h4>{{ note.title }}</h4>
      <button type="button" @click="$emit('restore', note.id)">Restore</button>
    </li>
  </ul>
</template>

<script>
export default {
  props: { archivedNotes: { type: Array, default: () => [] } },
  emits: ["restore"],
};
</script>
