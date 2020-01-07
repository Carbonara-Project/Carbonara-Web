<template>
<div class="row">
  <div class="col s12">
    <proc-info
      v-bind:md5="md5"
      v-bind:procInfo="procInfo"
      v-bind:procSimilar="procSimilar"
    >
    </proc-info>
  </div>
  <div class="col s12">
    <proc-desc-list
      v-bind:procDescs="procDescs"
      v-on:procDescSelection="procDescSelection"
    >
    </proc-desc-list>
  </div>
</div>  
</template>
<script>
import api from '../../api/api'
import ProcInfo from './ProcInfo'
import ProcDescList from './ProcDescList'

const breadcrumbs = [
    {label: 'Dashboard', path: '/'},
    {label: 'Procedure', path: ''}
]

export default {
  name: 'procedure',
  components: {
    ProcInfo,
    ProcDescList
  },
  data() {
    return {
      md5: this.$route.params.md5
    }
  },
  watch: {
    '$route': function() {
      this.fetchData()
    }
  },
  computed: {
    procDescs() {
      return this.$store.state.ProcDescs
    },
    procInfo() {
      return this.$store.state.SelectedProcDesc
    },
    procSimilar() {
      return this.$store.state.ProcSimilar
    }
  },
  methods: {
    fetchData() {
      api.procedureDescs(this.$route.params.md5, this.$route.params.offset)
    },
    // This calls procedureSimilar with most rated proc_desc_id
    fetchSimilar(desc_id) {
      api.procedureSimilar(this.$route.params.md5, this.$route.params.offset, this.procInfo)
    },
    procDescSelection(procDescID) {
      // Map the procDescID to the index of it in the ProcDescList
      let index = 0
      for (let i = 0; i < this.$store.state.ProcDescs.length; i++) {
        const element = this.$store.state.ProcDescs[i];
        if (element.id == procDescID) {
          index = i
          break
        }
      }
      this.$store.commit('updateSelectedProcDesc', this.$store.state.ProcDescs[index])
    }
  },
  created() {
    this.$store.commit('updateBreadcrumbs', {breadcrumbs: breadcrumbs})
    this.fetchData()
  }
}
</script>
<style lang="scss" scoped>

</style>
