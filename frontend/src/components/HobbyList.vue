<template>
  <div>
    <!-- new hobby form -->
    <div class="new-hobby-form">
      <HobbyForm />
    </div>

    <!-- filter -->
    <nav class="filter">
      <button @click.prevent="filter = 'user'">My hobbies</button>
      <button @click.prevent="filter = 'all'">All hobbies</button>
    </nav>

    <!-- hobby list -->
    <div class="hobby-list" v-if="filter === 'all'">
      <p>There are {{ hobbyStore.totalCount }} hobbies</p>
      <div v-for="hobby in hobbyStore.hobbies" :key="hobby.url">
        <HobbyItem :hobby="hobby" />
      </div>
    </div>

    <div class="hobby-list" v-if="filter === 'user'">
      <p>You have {{ hobbyStore.favCount }} hobbies</p>
      <div v-for="hobby in hobbyStore.userHobbies" :key="hobby.url">
        <HobbyItem :hobby="hobby" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useHobbyStore } from "../stores/HobbyStore";
import HobbyItem from "./HobbyItem.vue";
import HobbyForm from "./HobbyForm.vue";

// Define a type for the filter
type Filter = "user" | "all";

export default defineComponent({
  name: "Hobbies",
  components: { HobbyItem, HobbyForm },
  setup() {
    // Access the hobby store
    const hobbyStore = useHobbyStore();
    hobbyStore.getHobbies();

    // Filter state
    const filter = ref<Filter>("all");

    return {
      hobbyStore,
      filter,
    };
  },
});
</script>
