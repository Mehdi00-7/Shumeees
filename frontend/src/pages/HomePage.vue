<template>
  <div>
    <p>
      Shumeees is a hobby-based web application. This social network allows
      users to create profiles and connect with others based on shared hobbies.
    </p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { usePageStore } from "../stores/PageStore";
import { useProfilePageStore } from "../stores/ProfilePageStore";

export default defineComponent({
  name: "HomePage",
  setup() {
    // Access Pinia stores
    const pageStore = usePageStore();
    const profilePageStore = useProfilePageStore();

    // Update page title and button visibility
    pageStore.setHomeTitle();
    profilePageStore.setButtonVisibilityOff();

    return {};
  },
});
</script>
