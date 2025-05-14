import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../pages/HomePage.vue";
import ProfileEditPage from "../pages/profile/ProfileEditPage.vue";
import ProfileViewPage from "../pages/profile/ProfileViewPage.vue";
import UsersPage from "../pages/UsersPage.vue";
import FriendsPage from "../pages/FriendsPage.vue";

const routes = [
  { path: "/", component: HomePage },
  { path: "/profile-edit", component: ProfileEditPage },
  { path: "/profile-view", component: ProfileViewPage },
  { path: "/users", component: UsersPage },
  { path: "/friends", component: FriendsPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
