<template>
  <main>
    <!-- nav -->
    <nav class="navbar navbar-expand-lg">
      <div class="nav-container">
        <button class="button-1" @click="goToHomePage">Shumeees</button>

        <div
          class="collapse navbar-collapse"
          :class="{ show: isNavbarCollapsed }"
          id="navbarNav"
        >
          <button class="button-2" @click="goToProfileViewPage">Profile</button>
          <button class="button-2" @click="goToUsersPage">Users</button>
          <button class="button-2" @click="goToFriendsPage">Friends</button>
          <button class="logout" @click="logout">Log out</button>
        </div>

        <button
          class="navbar-toggler"
          type="button"
          @click="toggleNavbar"
          aria-controls="navbarNav"
          :aria-expanded="isNavbarCollapsed"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
      </div>
    </nav>
    <!-- heading -->
    <header>
      <div class="header-container">
        <img src="./assets/hobbies.png" alt="hobbies logo" />
        <h1>{{ pageStore.currentPageTitle }}</h1>
      </div>

      <div v-if="profilePageStore.isProfileButtonVisible">
        <button class="button-3" @click="handleProfileAction">
          {{ profilePageStore.currentProfilePageText }}
        </button>
      </div>
    </header>

    <router-view />
  </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { usePageStore } from "./stores/PageStore";
import { useProfilePageStore } from "./stores/ProfilePageStore";
import HobbyItem from "./components/HobbyItem.vue";
import HobbyForm from "./components/HobbyForm.vue";
import { getCsrfToken } from "./utils";

export default defineComponent({
  name: "MainComponent",
  components: { HobbyItem, HobbyForm },
  setup() {
    const pageStore = usePageStore();
    const profilePageStore = useProfilePageStore();

    return { pageStore, profilePageStore };
  },
  data() {
    return {
      isNavbarCollapsed: true,
      isHobbyListVisible: false,
    };
  },
  methods: {
    toggleNavbar(): void {
      this.isNavbarCollapsed = !this.isNavbarCollapsed;
    },
    async logout(): Promise<void> {
      await fetch("/auth/logout/", {
        method: "POST",
        headers: {
          "X-CSRFToken": getCsrfToken(),
        },
      });
      window.location.replace("/");
    },
    handleProfileAction(): void {
      if (this.profilePageStore.isProfileEditButtonOn) {
        this.goToProfileEditPage();
      } else {
        this.goToProfileViewPage();
      }
    },
    goToHomePage(): void {
      this.$router.push("/");
    },
    goToProfileEditPage(): void {
      this.$router.push("/profile-edit");
    },
    goToProfileViewPage(): void {
      this.$router.push("/profile-view");
    },
    goToUsersPage(): void {
      this.$router.push("/users");
    },
    goToFriendsPage(): void {
      this.$router.push("/friends");
    },
  },
});
</script>
