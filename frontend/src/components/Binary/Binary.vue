<template>
  <div>
    <div class="row">
      <div class="col s12 m6 offset-m3">
        <h4 class="info-header cyan-darken3">Info</h4>
        <info-list v-bind:info="binary.info"></info-list>
      </div>
    </div>
    <div class="row">
      <div class="col s12 m6 offset-m3">
        <h4 class="comments-header cyan-darken3">Comments</h4>
        <binary-comment-list 
          v-bind:binaryId="this.md5"
          v-bind:isSelected="true"></binary-comment-list>
      </div>
    </div>
    <div class="row">
      <div class="col s12 m6 offset-m3">
        <h4 class="cyan-darken3">Procedures</h4>
        <procedure-list v-bind:md5="md5" v-bind:procs="binary.procs"></procedure-list>
      </div>
    </div>
  </div>
</template>

<script>
  import api from '../../api/api'
  import ProcedureList from './ProcedureList'
  import InfoList from './BinaryInfo'
  import BinaryCommentList from './BinaryCommentList'
  
  const breadcrumbs = [{
      label: 'Dashboard',
      path: '/'
    },
    {
      label: 'Binary',
      path: ''
    }
  ]
  
  export default {
    name: 'binary',
    components: {
      ProcedureList,
      InfoList,
      BinaryCommentList
    },
    data() {
      return {
        md5: this.$route.params.md5
      }
    },
    computed: {
      binary: function() {
        return this.$store.state.Binary
      }
    },
    watch: {
      '$route': function() {
        this.fetchData()
      }
    },
    methods: {
      fetchData() {
        api.programInfo(this.md5)
        api.programCommentList(this.md5)
      }
    },
    created() {
      this.$store.commit('updateBreadcrumbs', {
        breadcrumbs: breadcrumbs
      })
      this.fetchData()
    }
  
  }
</script>

<style lang="scss" scoped>

  .cyan-darken3 {
    color: #00838f !important;
  }

  .info-header{
    margin-top:1.5em;
  }
  
</style>
