<template>
  <router-link :to="'/user/' + email">
    <div v-if="showName" class="chip">
      <img :src="imageUrl" alt="Contact Person">
      <span>{{ email }}</span>
    </div>  
    <img v-else class="circle" :src="imageUrl" alt="Contact Person">
  </router-link>
</template>
<script>
import usersApi from "../../api/users.js";

export default {
  name: "user-badge",
  props: {
    email: String,
    showName: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      imageUrl: ""
    };
  },
  mounted() {
    let _this = this;
    usersApi.retrieveProfileImg(this.email)
      .then(function(response) {
        _this.imageUrl = response.data.profile_image;
      })
      .catch(function(error) {
        console.log(error);
      });
  }
};
</script>
<style lang="scss" scoped>
.chip {
  a {
    color: rgba(0, 0, 0, 0.6);
  }
}
img {
  width: 32px;
  height: 32px;
}
</style>
