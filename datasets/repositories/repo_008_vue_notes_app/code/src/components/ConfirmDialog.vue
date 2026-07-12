<template>
  <div class="confirm-dialog" v-if="open">
    <p>{{ message }}</p>
    <button type="button" @click="$emit('confirm')">Yes</button>
    <button type="button" @click="$emit('cancel')">Cancel</button>
  </div>
</template>

<script>
export default {
  props: {
    open: { type: Boolean, default: false },
    message: { type: String, default: "Are you sure?" },
  },
  emits: ["confirm", "cancel"],
};
</script>
