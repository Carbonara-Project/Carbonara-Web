<template>

<div class="row">
    <div class="col s12">
        <table class="bordered highlight responsive-table">
        <thead>
          <tr>
              <th></th>
              <th></th>
          </tr>
        </thead>

        <tbody>
            <tr v-for="(value,key,index) in mInfo[0]" v-bind:key="index">
                <td><b>{{ key }}</b></td>
                <td>{{ value }}</td>
            </tr>
        </tbody>
      </table>
    </div>
</div>
</template>
<script>
export default {
  name: "binary-info",
  props: ["info"],
  computed: {
    mInfo() {
      return this.info || {};
    }
  }
};
</script>