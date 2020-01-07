<template>
<div> <!-- Generic div -->
  <div class="row">
    <div class="col s12">
      <ul class="collection">
        <li class="collection-item row" v-for='p in mProcs' v-bind:key='p.offset'>
          <div class="info col s11">
            <i class="material-icons left">code</i>
            <code>
              <router-link v-bind:to="getProcLink(p)" >
                <span class="name" v-if="p.name_proc">[{{ p.name_proc }}]</span>
                <span class="offset new badge right fixcolor" data-badge-caption="">0x{{ p.offset.toString(16) }}</span>
              </router-link>
              <span v-if="p.md5">@</span>
              <router-link class="binary-name" v-if="p.md5" :to="'/binary/' + p.md5">
                {{ p.name_bin }}
              </router-link>
            </code>
          </div>
          <div v-if="p.match" class="col s1">
            <span class="new badge" data-badge-caption="%">{{ p.match }}</span>
          </div>
        </li>
        <li v-if='mProcs.length == 0'> No procedures found</li>
      </ul>
    </div>
  </div>
</div>
</template>

<script>
  export default {
    name: "procedure-list",
    props: ['md5', 'procs'],
    computed: {
      mProcs() {
        return this.procs || []
      }
    },
    methods: {
      getProcLink(proc) {
        return '/binary/' + (this.md5 || proc.md5) + '/' + proc.offset
      }
    }
  };
</script>

<style lang="scss">
.fixcolor {
  background-color: #135e8d !important;
}
li {
  .info {
    display: flex;
    align-items: center;
    code {
      margin-left: 8px;
      margin-right: 8px;
      width: 100%;
    }
  }
}
</style>
