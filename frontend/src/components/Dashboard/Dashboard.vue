<template>
<div>
    <search-bar></search-bar>
    <upload></upload>
    <trending></trending>
    <div class="fixed-action-btn">
        <!-- <router-link to='/upload'>
            <transition name="slide-fade-up">
                <a v-if="mounted" class="btn-floating btn-large waves-effect waves-light cyan darken-4">
                    <i class="material-icons">add</i>
                </a>
            </transition>
        </router-link> -->
    </div>
</div>
</template>

<script>
import SearchBar from './SearchBar'
import Trending from './Trending'
import Upload from '../Upload'

const breadcrumbs = [
    {label: 'Dashboard', path: '/'}
]

export default {
  name: 'dashboard',
  components: {
      SearchBar,
      Upload,
      Trending
  },
  data () {
    return {
        mounted: false
    }
  },
  computed: {
      profileLink: function() { return '/user/' + localStorage.getItem('username') }
  },
  mounted: function() {
      this.$store.commit('updateBreadcrumbs', {breadcrumbs: breadcrumbs});
      
      let _this = this;
      setTimeout(function() {
          _this.mounted = true;
      });
  }
}
</script>

<style lang="scss">
.form-section {
  padding-left: 16px;
  padding-right: 16px;
}

.slide-fade-up-enter-active {
  transition: all .3s ease-in-out;
}
.slide-fade-up-leave-active {
  transition: all .3s ease-in-out;
}
.slide-fade-up-enter, .slide-fade-up-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  transform: translateY(20px);
  opacity: 0;
}
</style>
