import { defineStore } from "pinia";

// Define the state interface
interface PageState {
  currentPageTitle: string;
}

// Define the store with types
export const usePageStore = defineStore("page", {
  state: (): PageState => ({
    currentPageTitle: "",
  }),
  actions: {
    setHomeTitle(): void {
      this.currentPageTitle = "Shumeees";
    },
    setProfileTitle(): void {
      this.currentPageTitle = "Profile";
    },
    setUsersTitle(): void {
      this.currentPageTitle = "Users";
    },
    setFriendsTitle(): void {
      this.currentPageTitle = "Friends";
    },
  },
});
