<template>
  <div class="row">
        <div class="col s12 m6 offset-m3">
            <div class="search-wrapper card">
                <!-- TODO: Implement search by name or MD5/SHA256 -->
                <!-- <div class="switch">
                    <label>
                        Off
                    <input type="checkbox">
                    <span class="lever"></span>
                        On
                    </label>
                </div> -->
                <input id="search-input" placeholder="Search for program by MD5 or by name (prefixing '@')">
                <i class="material-icons">search</i>
                <div class="search-results">
                  <ul>
                    <li v-for="binary in md5Results" v-bind:key="binary.md5">
                      <router-link
                        v-bind:to="getBinaryLink(binary.md5)"
                      >
                        <b> MD5: </b>{{ binary.md5 }}
                      </router-link>
                    </li>
                    <li v-for="binary in nameResults" v-bind:key="binary.md5">
                      <router-link
                        v-bind:to="getBinaryLink(binary.md5)"
                      >
                        <b> NAME: </b> {{ binary.filename }}
                      </router-link>
                    </li>
                  </ul>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import api from '../../api/api'
export default {
  name: 'search-bar',
  computed: {
    md5Results: function() { return this.$store.state.MD5SearchResult },
    nameResults: function() { return this.$store.state.NameSearchResult }
  },
  methods: {
    getBinaryLink(md5) {
      return "/binary/" + md5.toLowerCase()
    }
  },
  mounted() {
    // Clear old searches
    this.$store.commit('loadMD5SearchResult', []);
    this.$store.commit('loadNameSearchResult', []);
    // Search
    document.querySelector('#search-input').addEventListener('keyup', (e) => {
      this.$store.commit('loadMD5SearchResult', []);
      this.$store.commit('loadNameSearchResult', []);
      let search = e.target.value.trim()
      if (search.length === 0) {
        return;
      }
      if (search[0] === '@' && search.length > 1){
        name = search.substring(1);
        api.searchProgramBy(name, 'name');
      }
      else if (search[0] !== '@'){
        api.searchProgramBy(search, 'md5');
      }
      else {
        return;
      }
      // TODO: Considering if adding this back
      // document.querySelectorAll('.search-wrapper li').forEach(e => {
      //   let content = e.textContent.trim()
      //   let from = content.indexOf(search)
      //   // This shuold definitely not happen since we 
      //   // look for malware starting with search text
      //   if (from != 0) {
      //     e.innerHTML = e.textContent
      //     return;
      //   }
      //   let to = from + search.length
      //   let targetText = content.substring(from, to)
      //   let remainingText = content.substring(to, to + content.length - targetText.length)
      //   e.innerHTML = '<mark style="background-color: transparent">' + targetText + '</mark>' + remainingText
      // })
    })
  }
}
</script>
<style lang="scss" scoped>
.search-wrapper {
  margin-top:40px;
  #search-input {
      display: block;
      font-size: 16px;
      font-weight: 300;
      width: 100%;
      height: 45px;
      margin: 0;
      -webkit-box-sizing: border-box;
      box-sizing: border-box;
      padding: 0 45px 0 15px;
      border: 0
  }
  #search-input + i{
      position: absolute;
      top: 10px;
      right: 10px;
  }

  .search-results {
    padding: 0 16px; 
    ul { margin: 0; padding: 0; }
    li {
      padding: 8px 0;
      color: lightgray;
    }
  }
}
</style>

