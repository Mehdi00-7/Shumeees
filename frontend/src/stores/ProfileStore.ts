import { defineStore } from "pinia";
import { getCsrfToken } from "../utils";

interface ProfileState {
  url: string;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  date_of_birth: string;
  age: number | null;
  hobbies: string[];
  loadingProfile: boolean;
  loadingAllHobbies: boolean;
}

export const useProfileStore = defineStore("profileStore", {
  state: (): ProfileState => ({
    url: "",
    username: "",
    first_name: "",
    last_name: "",
    email: "",
    date_of_birth: "",
    age: null,
    hobbies: [],
    loadingProfile: false,
    loadingAllHobbies: false,
  }),
  actions: {
    async getProfile() {
      this.loadingProfile = true;
      const res = await fetch(`/api/users/current/`);
      const data = await res.json();

      this.url = data.url;
      this.username = data.username;
      this.first_name = data.first_name;
      this.last_name = data.last_name;
      this.email = data.email;
      this.date_of_birth = data.date_of_birth;
      this.age = data.age;
      this.hobbies = data.hobbies;
      this.loadingProfile = false;
    },
    async saveProfile(updatedProfile: {
      first_name: string;
      last_name: string;
      email: string;
      date_of_birth: string;
    }) {
      try {
        const response = await fetch("/api/users/current/", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify({
            username: this.username,
            first_name: updatedProfile.first_name,
            last_name: updatedProfile.last_name,
            email: updatedProfile.email,
            date_of_birth: updatedProfile.date_of_birth,
          }),
        });

        const data = await response.json();
        console.log("Profile updated successfully:", data);
      } catch (error) {
        console.error("Failed to save profile:", error);
      }
    },
  },
});
