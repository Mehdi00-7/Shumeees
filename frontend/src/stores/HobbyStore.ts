import { defineStore } from "pinia";
import { getCsrfToken } from "../utils";

interface Hobby {
  url: string;
  name: string;
  isFav: boolean;
}

interface HobbyResponse {
  results: Hobby[];
}

interface UserResponse {
  username: string;
  hobbies: string[];
  hobby_list: { url: string; name: string }[];
}

interface HobbyState {
  hobbies: Hobby[];
  userHobbies: Hobby[];
  loading: boolean;
}

export const useHobbyStore = defineStore("hobbyStore", {
  state: (): HobbyState => ({
    hobbies: [],
    userHobbies: [],
    loading: false,
  }),
  getters: {
    myHobbies(state): Hobby[] {
      return state.hobbies.filter((hobby) => hobby.isFav);
    },
    favCount(state): number {
      return state.userHobbies.reduce(
        (count, hobby) => (hobby.isFav ? count + 1 : count),
        0,
      );
    },
    totalCount: (state): number => {
      return state.hobbies.length;
    },
  },
  actions: {
    async getHobbies(): Promise<void> {
      this.loading = true;
      try {
        // Fetch all hobbies
        const res = await fetch("/api/hobbies/");
        if (!res.ok) {
          throw new Error(`Failed to fetch hobbies: ${res.statusText}`);
        }
        const data: HobbyResponse = await res.json();
        this.hobbies = data.results;

        // Fetch user-specific hobbies
        const res2 = await fetch("/api/users/current/");
        if (!res2.ok) {
          throw new Error(`Failed to fetch user's hobbies: ${res2.statusText}`);
        }
        const data2: UserResponse = await res2.json();

        // Map user hobbies to include the `isFav` flag
        this.userHobbies = data2.hobby_list.map((hobby) => ({
          ...hobby,
          isFav: true,
        }));

        // Mark hobbies as favorites if they are in the user's hobby list
        this.hobbies.forEach((hobby) => {
          if (
            this.userHobbies.some((userHobby) => userHobby.url === hobby.url)
          ) {
            hobby.isFav = true;
          }
        });

        this.loading = false;
      } catch (error) {
        console.error("Failed to show user hobbies:", error);
        this.loading = false;
      }
    },

    async addHobby(hobbyName: string): Promise<void> {
      try {
        const response = await fetch("/api/hobbies/", {
          method: "POST",
          body: JSON.stringify({ name: hobbyName }),
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
        });

        const data = await response.json();
        console.log("Hobbies updated successfully:", data);
        this.getHobbies();
      } catch (error) {
        console.error("Failed to save hobby:", error);
      }
    },

    async toggleHobby(hobby: Hobby): Promise<void> {
      if (hobby.isFav) {
        await this.deleteHobby(hobby);
      } else {
        await this.addToMyHobbies(hobby);
      }
    },

    async deleteHobby(hobby: Hobby): Promise<void> {
      try {
        const res = await fetch("/api/users/current/");
        if (!res.ok) {
          throw new Error(`Failed to fetch user's hobbies: ${res.statusText}`);
        }
        const data: UserResponse = await res.json();

        // Remove the hobby from the user's list
        const updatedHobbies = data.hobbies.filter((url) => url !== hobby.url);

        const res1 = await fetch(`/api/users/current/`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify({
            username: data.username,
            hobbies: updatedHobbies,
          }),
        });

        if (!res1.ok) {
          console.error("Failed to delete hobby:", await res1.text());
        }

        await this.getHobbies();
      } catch (error) {
        console.error("Failed to delete hobby:", error);
      }
    },

    async addToMyHobbies(hobby: Hobby): Promise<void> {
      try {
        const res = await fetch("/api/users/current/");
        if (!res.ok) {
          throw new Error(`Failed to fetch user's hobbies: ${res.statusText}`);
        }
        const data: UserResponse = await res.json();

        // Add the new hobby to the user's list
        const updatedHobbies = [...data.hobbies, hobby.url];

        const response = await fetch("/api/users/current/", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify({
            username: data.username,
            hobbies: updatedHobbies,
          }),
        });

        if (!response.ok) {
          throw new Error(`Failed to add hobby: ${response.statusText}`);
        }

        const data3 = await response.json();
        console.log("Hobbies updated successfully:", data3);

        await this.getHobbies();
      } catch (error) {
        console.error("Failed to save hobby:", error);
      }
    },
  },
});
