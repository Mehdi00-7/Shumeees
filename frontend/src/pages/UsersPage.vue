<template>
  <main>
    <div class="content">
      <div class="filters">
        <label for="min-age">Min Age:</label>
        <input
          type="number"
          id="min-age"
          v-model="minAge"
          @change="fetchUsers"
          placeholder="Min Age"
        />

        <label for="max-age">Max Age:</label>
        <input
          type="number"
          id="max-age"
          v-model="maxAge"
          @change="fetchUsers"
          placeholder="Max Age"
        />
      </div>

      <UsersTable :users="users" />

      <div class="pagination">
        <button @click="previousPage" :disabled="currentPage <= 1">
          Previous
        </button>
        <span>Page {{ currentPage }}</span>
        <button @click="nextPage" :disabled="!nextPageAvailable">Next</button>
      </div>
    </div>
  </main>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted } from "vue";
import UsersTable from "../components/UsersTable.vue";
import { usePageStore } from "../stores/PageStore";
import { useProfilePageStore } from "../stores/ProfilePageStore";

interface Hobby {
  name: string;
  url: string;
}

interface User {
  url: string;
  username: string;
  hobby_list: Hobby[];
  received_friend_requests: string[];
}

interface UserResponse {
  results: User[];
  count: number;
}

export default defineComponent({
  name: "UsersPage",
  components: {
    UsersTable,
  },
  setup() {
    const pageStore = usePageStore();
    const profilePageStore = useProfilePageStore();

    // Update page title and button visibility
    pageStore.setUsersTitle();
    profilePageStore.setButtonVisibilityOff();

    // Reactive properties
    const users = ref<User[]>([]);
    const minAge = ref<number | null>(null);
    const maxAge = ref<number | null>(null);
    const currentPage = ref<number>(1);
    const totalUsers = ref<number>(0);
    const usersPerPage = 10;

    // Computed properties
    const nextPageAvailable = computed(
      () => users.value.length === usersPerPage,
    );

    // Fetch users
    const fetchUsers = async () => {
      try {
        const response = await fetch(
          `/api/users/?min_age=${minAge.value || ""}&max_age=${maxAge.value || ""}&page=${currentPage.value}`,
          {
            headers: {
              "Content-Type": "application/json",
            },
          },
        );

        if (!response.ok) {
          console.error("Error fetching users:", response.statusText);
          return;
        }

        const data: UserResponse = await response.json();
        users.value = data.results;
        totalUsers.value = data.count;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };

    // Pagination controls
    const nextPage = () => {
      if (nextPageAvailable.value) {
        currentPage.value++;
        fetchUsers();
      }
    };

    const previousPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--;
        fetchUsers();
      }
    };

    // Fetch users on mount
    onMounted(() => {
      fetchUsers();
    });

    // Return reactive properties and methods
    return {
      users,
      minAge,
      maxAge,
      currentPage,
      totalUsers,
      nextPageAvailable,
      fetchUsers,
      nextPage,
      previousPage,
    };
  },
});
</script>

<style scoped>
.filters {
  margin-bottom: 10px;
}

.pagination {
  margin-top: 20px;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
