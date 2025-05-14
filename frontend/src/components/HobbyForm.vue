<template>
  <form @submit.prevent="handleSubmit">
    <input type="text" placeholder="I like..." v-model="newHobby" />
    <button type="submit">Add</button>
  </form>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useHobbyStore } from "../stores/HobbyStore";

export default defineComponent({
  name: "HobbyForm",
  setup() {
    // Access the hobby store
    const hobbyStore = useHobbyStore();

    // New hobby input
    const newHobby = ref<string>("");

    // Handle form submission
    const handleSubmit = (): void => {
      if (newHobby.value.trim().length > 0) {
        hobbyStore.addHobby(newHobby.value.trim());
        newHobby.value = "";
      }
    };

    return { handleSubmit, newHobby };
  },
});
</script>
