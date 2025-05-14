import { defineStore } from "pinia";
import { getCsrfToken } from "../utils";

// Define types for friends and friend requests
interface Friend {
  url: string;
  username: string;
}

interface UserResponse {
  url: string;
  username: string;
  friends: string[]; // URLs of friends
  received_friend_requests: string[]; // URLs of friend requests
}

export const useFriendStore = defineStore("friend", {
  state: () => ({
    friends: [] as Friend[],
    friendRequests: [] as Friend[],
  }),
  actions: {
    async fetchFriends(): Promise<void> {
      try {
        const response = await fetch("/api/users/current/");
        if (!response.ok) {
          throw new Error("Failed to fetch current user");
        }

        const user: UserResponse = await response.json();

        // Fetch friends details
        const friendsPromises = user.friends.map(async (friendUrl: string) => {
          const friendResponse = await fetch(friendUrl);
          if (!friendResponse.ok) {
            throw new Error(`Failed to fetch friend from ${friendUrl}`);
          }

          const friend = await friendResponse.json();
          return { url: friend.url, username: friend.username };
        });

        this.friends = await Promise.all(friendsPromises);
      } catch (error) {
        console.error("Error fetching friends:", error);
      }
    },

    async fetchFriendRequests(): Promise<void> {
      try {
        const response = await fetch("/api/users/current/");
        if (!response.ok) {
          throw new Error("Failed to fetch current user");
        }

        const user: UserResponse = await response.json();

        // Fetch friend requests details
        const friendRequestsPromises = user.received_friend_requests.map(
          async (requestUrl: string) => {
            const requestResponse = await fetch(requestUrl);
            if (!requestResponse.ok) {
              throw new Error(
                `Failed to fetch friend request from ${requestUrl}`,
              );
            }

            const request = await requestResponse.json();
            return { url: request.url, username: request.username };
          },
        );

        this.friendRequests = await Promise.all(friendRequestsPromises);
      } catch (error) {
        console.error("Error fetching friend requests:", error);
      }
    },

    async acceptFriendRequest(url: string): Promise<void> {
      console.log(url);
      try {
        const res = await fetch("/api/users/current/");
        if (!res.ok) {
          throw new Error("Failed to fetch current user");
        }

        const user: UserResponse = await res.json();

        const response = await fetch("/api/users/current/", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify({
            username: user.username,
            received_friend_requests: user.received_friend_requests.filter(
              (requestUrl: string) => requestUrl !== url,
            ),
            friends: [...user.friends, url],
          }),
        });

        if (!response.ok) {
          throw new Error("Failed to accept friend request");
        }

        // Refresh data
        await this.fetchFriends();
        await this.fetchFriendRequests();
      } catch (error) {
        console.error("Error accepting friend request:", error);
      }
    },

    async declineFriendRequest(url: string): Promise<void> {
      try {
        const res = await fetch("/api/users/current/");
        if (!res.ok) {
          throw new Error("Failed to fetch current user");
        }

        const user: UserResponse = await res.json();

        const response = await fetch("/api/users/current/", {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify({
            username: user.username,
            received_friend_requests: user.received_friend_requests.filter(
              (requestUrl: string) => requestUrl !== url,
            ),
            friends: user.friends,
          }),
        });

        if (!response.ok) {
          throw new Error("Failed to decline friend request");
        }

        // Refresh data
        await this.fetchFriendRequests();
      } catch (error) {
        console.error("Error declining friend request:", error);
      }
    },

    // New sendFriendRequest method
    async sendFriendRequest(url: string): Promise<void> {
      try {
        const res = await fetch("/api/users/current/");
        if (!res.ok) {
          throw new Error("Failed to fetch current user");
        }

        const currentUser: UserResponse = await res.json();

        const response = await fetch(url, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
          },
          body: JSON.stringify({
            received_friend_requests: [
              ...currentUser.received_friend_requests,
              currentUser.url,
            ],
          }),
        });

        if (!response.ok) {
          throw new Error("Failed to send friend request");
        }

        // Refresh friend request data
        await this.fetchFriendRequests();
      } catch (error) {
        console.error("Error sending friend request:", error);
      }
    },
  },
});
