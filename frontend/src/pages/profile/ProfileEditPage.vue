<template>
  <div>
    <form class="border p-4 rounded bg-light" @submit.prevent="handleSubmit">
      <!-- Loading Profile Data -->
      <div class="loadingProfile" v-if="loadingProfile">
        Loading profile data...
      </div>

      <!-- Name -->
      <div class="mb-3">
        <label for="first_name" class="form-label">First Name</label>
        <input
          type="text"
          id="first_name"
          class="form-control"
          v-model="first_name"
        />
      </div>
      <div class="mb-3">
        <label for="last_name" class="form-label">Last Name</label>
        <input
          type="text"
          id="last_name"
          class="form-control"
          v-model="last_name"
        />
      </div>
      <!-- Email -->
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input type="email" id="email" class="form-control" v-model="email" />
      </div>
      <!-- Date of Birth -->
      <div class="mb-3">
        <label for="date_of_birth" class="form-label">Date of Birth</label>
        <input
          type="date"
          id="date_of_birth"
          class="form-control"
          v-model="date_of_birth"
        />
      </div>

      <!-- Submit -->
      <button type="submit" class="btn btn-primary w-100">Save</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { storeToRefs } from "pinia";
import { useProfileStore } from "../../stores/ProfileStore";
import { usePageStore } from "../../stores/PageStore";
import { useProfilePageStore } from "../../stores/ProfilePageStore";

export default defineComponent({
  name: "ProfileEditPage",
  setup() {
    // Access stores
    const profileStore = useProfileStore();
    const pageStore = usePageStore();
    const profilePageStore = useProfilePageStore();

    // Extract reactive properties from the profile store
    const { first_name, last_name, email, date_of_birth, loadingProfile } =
      storeToRefs(profileStore);

    // Fetch profile and set page state
    profileStore.getProfile();
    pageStore.setProfileTitle();
    profilePageStore.setViewText();
    profilePageStore.setButtonVisibilityOn();
    profilePageStore.setViewButton();
    profilePageStore.setViewText();

    // Handle form submission
    const handleSubmit = async (): Promise<void> => {
      try {
        await profileStore.saveProfile({
          first_name: first_name.value,
          last_name: last_name.value,
          email: email.value,
          date_of_birth: date_of_birth.value,
        });

        // Reset fields after submission
        first_name.value = "";
        last_name.value = "";
        email.value = "";
        date_of_birth.value = "";
      } catch (error) {
        console.error("Failed to save profile:", error);
      }
    };

    return {
      loadingProfile,
      handleSubmit,
      first_name,
      last_name,
      email,
      date_of_birth,
    };
  },
});
</script>
