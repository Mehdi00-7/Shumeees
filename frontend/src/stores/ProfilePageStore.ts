import { defineStore } from "pinia";

// Define the state interface
interface ProfilePageState {
  currentProfilePageText: string;
  isProfileButtonVisible: boolean;
  isProfileEditButtonOn: boolean;
}

// Define the store with types
export const useProfilePageStore = defineStore("profilePage", {
  state: (): ProfilePageState => ({
    currentProfilePageText: "",
    isProfileButtonVisible: false,
    isProfileEditButtonOn: true,
  }),
  actions: {
    setButtonVisibilityOn(): void {
      this.isProfileButtonVisible = true;
    },
    setButtonVisibilityOff(): void {
      this.isProfileButtonVisible = false;
    },
    setEditButton(): void {
      this.isProfileEditButtonOn = true;
    },
    setViewButton(): void {
      this.isProfileEditButtonOn = false;
    },
    setEditText(): void {
      this.currentProfilePageText = "Edit Your Meees Profile";
    },
    setViewText(): void {
      this.currentProfilePageText = "View Your Meees Profile";
    },
  },
});
