<template>
  <meta name="csrf-token" content="{{ csrf_token }}" />
  <div>
    <h2>Your Friends</h2>
    <ul>
      <li v-for="friend in friendStore.friends" :key="friend.url">
        {{ friend.username }}
      </li>
    </ul>

    <h2>Friend Requests</h2>
    <ul>
      <li v-for="request in friendStore.friendRequests" :key="request.url">
        {{ request.username }}
        <button @click="friendStore.acceptFriendRequest(request.url)">
          Accept
        </button>
        <button @click="friendStore.declineFriendRequest(request.url)">
          Decline
        </button>
      </li>
    </ul>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { useFriendStore } from "../stores/FriendStore";
import { usePageStore } from "../stores/PageStore";
import { useProfilePageStore } from "../stores/ProfilePageStore";

export default defineComponent({
  name: "FriendsPage",
  setup() {
    // Access Pinia stores
    const friendStore = useFriendStore();
    const pageStore = usePageStore();
    const profilePageStore = useProfilePageStore();

    // Fetch data and update page settings
    onMounted(() => {
      friendStore.fetchFriends();
      friendStore.fetchFriendRequests();
    });

    pageStore.setFriendsTitle();
    profilePageStore.setButtonVisibilityOff();

    return {
      friendStore,
    };
  },
});
</script>

<style scoped></style>
