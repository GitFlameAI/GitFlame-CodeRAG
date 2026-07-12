<template>
  <input
    class="search-box"
    type="search"
    :value="modelValue"
    placeholder="Search notes..."
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>

<script>
export default {
  props: { modelValue: { type: String, default: "" } },
  emits: ["update:modelValue"],
};
</script>
