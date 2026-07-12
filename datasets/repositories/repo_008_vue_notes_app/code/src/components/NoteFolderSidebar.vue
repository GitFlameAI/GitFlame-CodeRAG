<template>
  <nav class="note-folder-sidebar">
    <ul>
      <li
        v-for="folder in folders"
        :key="folder"
        :class="{ active: folder === activeFolder }"
        @click="$emit('select', folder)"
      >
        {{ folder }}
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  props: {
    folders: { type: Array, default: () => ["All", "Personal", "Work"] },
    activeFolder: { type: String, default: "All" },
  },
  emits: ["select"],
};
</script>
