<template>
  <div class="hobby">
    <div>{{ hobby.name }}</div>
    <div class="icons">
      <i
        class="material-icons"
        :class="{ active: hobby.isFav }"
        @click="toggleFavorite"
      >
        favorite
      </i>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { useHobbyStore } from "../stores/HobbyStore";

interface Hobby {
  name: string;
  url: string;
  isFav: boolean;
}

export default defineComponent({
  name: "HobbyItem",
  props: {
    hobby: {
      type: Object as PropType<Hobby>,
      required: true,
    },
  },
  setup(props) {
    const hobbyStore = useHobbyStore();

    const toggleFavorite = () => {
      hobbyStore.toggleHobby(props.hobby);
    };

    return { toggleFavorite };
  },
});
</script>
