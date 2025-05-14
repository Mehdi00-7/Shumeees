<template>
  <div>
    <h2>All Users</h2>
    <div v-for="user in users" :key="user.url">
      <p>{{ user.username }}</p>
      <button @click="sendFriendRequest(user.url)">Send Friend Request</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import { useFriendStore } from "../stores/FriendStore";

// Define the structure of the user data
interface User {
  url: string;
  username: string;
}

export default defineComponent({
  name: "AllUsers",
  setup() {
    // Define reactive properties
    const users = ref<User[]>([]);

    // Access FriendStore
    const friendStore = useFriendStore();

    // Fetch users from the API
    const fetchUsers = async (): Promise<void> => {
      const response = await fetch("/api/users/");
      if (response.ok) {
        users.value = await response.json();
      } else {
        console.error("Failed to fetch users");
      }
    };

    // Send a friend request
    const sendFriendRequest = async (url: string): Promise<void> => {
      try {
        await friendStore.sendFriendRequest(url);
        alert("Friend request sent");
      } catch (error) {
        console.error("Failed to send friend request:", error);
        alert("Error sending friend request.");
      }
    };

    // Fetch users when the component is mounted
    fetchUsers();

    return {
      users,
      sendFriendRequest,
    };
  },
});
</script>

<style scoped>
table {
  /* Outer border */
  border: 2px solid #333;
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #333;
  padding-top: 5px;
  padding-bottom: 5px;
  padding-left: 10px;
  padding-right: 10px;
}
</style>
