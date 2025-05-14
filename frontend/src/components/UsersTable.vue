<template>
  <meta name="csrf-token" content="{{ csrf_token }}" />
  <div>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Username</th>
          <th>Top Hobbies</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.url">
          <td>{{ user.username }}</td>
          <td>
            <ul>
              <!-- Render hobby names from hobby_list -->
              <li
                v-for="(hobby, index) in user.hobby_list.slice(0, 3)"
                :key="index"
              >
                {{ hobby.name }}
              </li>
              <li v-if="!user.hobby_list.length">No hobbies</li>
            </ul>
          </td>
          <td>
            <button
              v-if="
                user.url !== profileStore.url &&
                !friendStore.friends
                  .map((friend) => friend.username)
                  .includes(user.username)
              "
              @click="sendFriendRequest(user.url)"
              :disabled="
                user.received_friend_requests.includes(profileStore.url)
              "
            >
              {{
                user.received_friend_requests.includes(profileStore.url)
                  ? "Request Sent"
                  : "Send Friend Request"
              }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { getCsrfToken } from "../utils";
import { useProfileStore } from "../stores/ProfileStore";
import { useFriendStore } from "../stores/FriendStore";

// Define user and hobby types for props
interface Hobby {
  name: string;
  url: string;
}

interface User {
  username: string;
  url: string;
  hobby_list: Hobby[];
  received_friend_requests: string[];
}

export default defineComponent({
  name: "UsersTable",
  props: {
    users: {
      type: Array as () => User[],
      required: true,
    },
  },
  setup() {
    // Access Pinia stores
    const profileStore = useProfileStore();
    const friendStore = useFriendStore();

    // Fetch profile and friends data
    profileStore.getProfile();
    friendStore.fetchFriends();

    return { profileStore, friendStore };
  },
  methods: {
    async sendFriendRequest(targetUrl: string): Promise<void> {
      try {
        // Extract the relative URL (if full URL is passed)
        const relativeUrl = targetUrl.replace(window.location.origin, "");

        // Fetch the current user's data
        const currentUserResponse = await fetch("/api/users/current/", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
        });

        if (!currentUserResponse.ok) {
          throw new Error("Failed to fetch current user data");
        }

        const currentUserData = await currentUserResponse.json();
        const currentUserUrl = currentUserData.url;

        // Fetch the target user's data
        const targetUserResponse = await fetch(relativeUrl, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
        });

        if (!targetUserResponse.ok) {
          throw new Error("Failed to fetch target user data");
        }

        const targetUserData = await targetUserResponse.json();

        // Update the target user's friend requests
        const updatedFriendRequests = [
          ...targetUserData.received_friend_requests,
          currentUserUrl,
        ];

        const updateResponse = await fetch(relativeUrl, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify({
            ...targetUserData,
            received_friend_requests: updatedFriendRequests,
          }),
        });

        if (!updateResponse.ok) {
          throw new Error("Failed to update target user data");
        }

        alert("Friend request sent!");
      } catch (error) {
        console.error("Error sending friend request:", error);
        alert("Failed to send friend request. Please try again.");
      }
    },
  },
});
</script>
