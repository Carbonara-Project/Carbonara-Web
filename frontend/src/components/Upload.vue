<template>
  <div>
    <div class="row">
      <div class="col s12 m6 offset-m3">
        <div>
          <h2 id="cyan-darken3">Upload a binary</h2>
        </div>
        <div>
          <p class="flow-text">The file will be analyzed by our servers to extract useful information.</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col s12 m6 offset-m3">
        <vue-dropzone ref="binaryUploadZone" id="dropzone" :options="dropzoneOptions" />
      </div>
    </div>
  </div>
</template>

<script>
  import vue2Dropzone from 'vue2-dropzone'
  import 'vue2-dropzone/dist/vue2Dropzone.css'
  
  import axiosClients from '../api/axiosClients.js'
  const normalAxios = axiosClients.normalAxios;
  
  const breadcrumbs = [{
      label: 'Dashboard',
      path: '/'
    },
    {
      label: 'Upload',
      path: ''
    }
  ]
  
  export default {
    name: 'upload',
    components: {
      vueDropzone: vue2Dropzone
    },
    data() {
      return {
        dropzoneOptions: {
          url: __API_HOST__ + '/api/program/',
          method: 'PUT',
          thumbnailWidth: 150,
          maxFilesize: 1,
          paramName: "binary",
          sending(file, xhr, formData) {
            // Add the Authorization right before the request is sent
            xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('access_token'));
            Materialize.toast("Check out your profile for the analysis", 3000, "rounded");
          }
        },
        //TODO: inizialize binary and db
        binary: "ciao",
        db: ""
      }
    },
    created: function() {
      this.$store.commit('updateBreadcrumbs', {
        breadcrumbs: breadcrumbs
      });
    }
  }
</script>

<style lang="scss">
  #cyan-darken3 {
    color: #00838f;
  }
  
  #centerText {
    margin-left: 10px;
  }
  
  .form-heading {
    margin-top: 64px;
    display: flex;
    flex-direction: column;
    align-items: center;
    img {
      border-radius: 50%;
      width: 100px;
      height: 100px;
    }
    h4 {
      text-align: center;
    }
  }
  
  .form-section {
    padding-left: 16px;
    padding-right: 16px;
    form {
      padding: 48px !important;
      padding-top: 32px !important;
      padding-bottom: 32px !important;
    }
    .button-container {
      display: flex;
      justify-content: center;
    }
  }
  
  footer {
    h6 {
      text-align: center;
    }
  }
</style>
