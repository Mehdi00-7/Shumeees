<template>
  <div class="pf-info">
    <table class="table table-striped">
      <thead>
        <tr>
          <th>Username</th>
          <th>First Name</th>
          <th>Last Name</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{ username }}</td>
          <td>{{ first_name }}</td>
          <td>{{ last_name }}</td>
        </tr>
      </tbody>
    </table>

    <table class="table table-striped">
      <thead>
        <tr>
          <th>Email</th>
          <th>Date of Birth</th>
          <th>Age</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{ email }}</td>
          <td>{{ date_of_birth }}</td>
          <td>{{ age }}</td>
        </tr>
      </tbody>
    </table>

    <HobbyList />
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { storeToRefs } from "pinia";
import { useHobbyStore } from "../../stores/HobbyStore";
import HobbyList from "../../components/HobbyList.vue";
import { useProfileStore } from "../../stores/ProfileStore";
import { usePageStore } from "../../stores/PageStore";
import { useProfilePageStore } from "../../stores/ProfilePageStore";

export default defineComponent({
  name: "ProfileViewPage",
  components: {
    HobbyList,
  },
  setup() {
    // Access Pinia stores
    const hobbyStore = useHobbyStore();
    const profileStore = useProfileStore();
    const pageStore = usePageStore();
    const profilePageStore = useProfilePageStore();

    // Extract state from ProfileStore using storeToRefs
    const { username, first_name, last_name, email, date_of_birth, age } =
      storeToRefs(profileStore);

    // Initialize stores and set page state
    hobbyStore.getHobbies();
    profileStore.getProfile();
    pageStore.setProfileTitle();
    profilePageStore.setButtonVisibilityOn();
    profilePageStore.setEditButton();
    profilePageStore.setEditText();

    return {
      username,
      first_name,
      last_name,
      email,
      date_of_birth,
      age,
      hobbyStore,
      profileStore,
    };
  },
});
</script>
