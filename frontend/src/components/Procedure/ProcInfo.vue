<template>
<div class="row">
    <div class="col s12 m6">
        <h4>Code</h4>
        <div class="code-container card-panel">
            <pre v-highlightjs="mProcInfo.asm"><code class="x86asm"></code></pre>
        </div>
    </div>
    <div class="col s12 m6">
        <div class="row">
            <div class="info-container col s12">
                <h4>Details</h4>
                <div class="info">
                    <i class="small material-icons">text_format</i>
                    <span>{{ mProcInfo.name }}</span>
                </div>
                <div class="info">
                    <i class="small material-icons">account_circle</i>
                    <router-link :to="'/user/' + mProcInfo.user">{{ mProcInfo.user }}</router-link>
                </div>
                <div class="info">
                    <i class="small material-icons">insert_drive_file</i>
                    <router-link :to="'/binary/' + md5">{{ md5 }}</router-link>
                </div>
            </div>
            <div class="col s12">
                <h5>Similar procedures</h5>
                <procedure-list
                    v-bind:procs="mProcSimilar"
                >
                </procedure-list>
            </div>
        </div>
    </div>
</div>  
</template>
<script>
import ProcedureList from '../Binary/ProcedureList'

export default {
  name: 'proc-info',
  components: {
      ProcedureList
  },
  props: ['md5', 'procInfo', 'procSimilar'],
  computed: {
      mProcInfo() {
          let placeholder = {
              asm: '-',
              user: '-',
              name: '-'
          }
          return this.procInfo || placeholder
      },
      mProcSimilar() {
          let placeholder = []
          return this.procSimilar || placeholder
      }
  }
}
</script>
<style lang="scss" scoped>
.code-container {
    pre {
        max-height: 70vh;
        .hljs {
            background-color: white;
        }
    }
}
.info-container {
    h4 {
        padding: 0 16px;
    }

    
    .info {
        display: flex;
        flex-direction: row;
        align-items: center;
        padding: 16px;

        span, a {
            padding: 0 8px;
        }

        a{
            color:#26a69a;
        }
    }
}
</style>
