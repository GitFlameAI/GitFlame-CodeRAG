<template>
  <ul class="tag-list">
    <li v-for="tag in tags" :key="tag">
      {{ tag }}
      <button type="button" @click="$emit('remove', tag)">x</button>
    </li>
  </ul>
</template>

<script>
export default {
  props: { tags: { type: Array, default: () => [] } },
  emits: ["remove"],
};
</script>
