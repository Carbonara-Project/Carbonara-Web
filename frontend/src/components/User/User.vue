<template>
    <div>
        <div class="row user-container">
            <div class="card-panel col s12 m8 offset-m2">
                <div class="row">
                    <div class="col s4 l2 profile-image" style="position: relative">
                        <img :src="profile_image" alt="" class="circle responsive-img">
                        <a class="waves-effect waves-light btn-small img-btn"  style="margin: auto !important; left: 50%; top: 50%; position: absolute; transform: translateX(-50%) translateY(-50%);">    
                        <vue-dropzone ref="binaryUploadZone" class="circle" id="customdropzone" :options="dropzoneOptions" :include-styling="false" v-on:vdropzone-success="saveProfileImage">
                        </vue-dropzone>
                        <label for="upload" class="light-green">
                                <i class="material-icons left img-btn" >camera_alt</i>
                            </label>
                        </a>
                    </div>
                    <template v-if="!modify">
                    <div class="row col s8 l10 user-info" style="position: relative">
                        <div class="col s12 l5 name-container">
                            <h6>Name</h6>
                            <h5>{{ full_name }}</h5>
                        </div>
                        <div class="col s12 l5 email-container">
                            <h6>Email</h6>
                            <h5>{{ username }}</h5>
                        </div>
                        <div class="col s12 bio-container">
                            <h6>Bio</h6>
                            <p>{{ bio }}</p>
                        </div>
                        <div class="col s12 setting-button" style="position: absolute; left:90%">
                            <a class="waves-effect waves-light btn-small" @click="editProfile">
                                <i class="material-icons left">settings</i>
                            </a>
                        </div>
                    </div>
                    </template>
                    <template v-else-if="modify">
                        <div class="row col s8 l10 user-info">
                            <div class="input-field col s6">
                                <input :value="first_name" id="first_name" type="text" class="validate">
                                <label for="first_name" v-bind:class="{active: first_name.length}">First Name</label>
                            </div>
                            <div class="input-field col s6">
                                <input :value="last_name" id="last_name" type="text" class="validate">
                                <label for="first_name" v-bind:class="{active: last_name.length}">Last Name</label>
                            </div>
                            <div class="input-field col s9">
                                <textarea :value="bio" id="bio" class="materialize-textarea"></textarea>
                                <label for="first_name" v-bind:class="{active: bio.length}">Bio</label>
                            </div>
                            <div class="input-field col s3">
                                <a class="waves-effect waves-light btn-small right fixMargin" @click="saveProfile"><i class="material-icons right">save</i>Save</a>
                            </div>
                        </div>
                    </template>
                </div>
                <!-- <div class="row">
                    <div class="col s12 m4">
                        <img :src="profile_image" alt="" class="circle responsive-img">
                    </div>
                    <div class="col s12 m8">
                        <div class="collection">
                            <div class="collection-item">
                                <i class="right material-icons center-icon">account_circle</i>
                                <h5>{{ full_name }}</h5>
                            </div>
                            <div class="collection-item">
                                <i class="right material-icons center-icon">mail</i>
                                <h5>{{ username }}</h5>
                            </div>
                        </div>
                        <div v-if="isSelf" class="right">
                            <button class="waves-effect waves-light btn btn-color" @click="logout">Logout</button>
                        </div>
                    </div>
                </div> -->
            </div>
        </div>
        <div v-if="isSelf" class="row transactions">
            <div class="col s12 m6 offset-m2">
                <transactions :transactions="transactions"></transactions>
            </div>
        </div>
    </div>
</template>

<script>
    import usersApi from '../../api/users'
    import api from '../../api/api'
    import Transactions from './Transactions'
    import vue2Dropzone from 'vue2-dropzone'
    import 'vue2-dropzone/dist/vue2Dropzone.css'
    
    const breadcrumbs = [{
            label: 'Dashboard',
            path: '/'
        },
        {
            label: 'User',
            path: ''
        }
    ]
    
    export default {
        name: 'user',
        data(){
            return {
                modify: false,
                dropzoneOptions: {
                    url: __API_HOST__ + '/users/profile/' + this.$store.state.User.username + '/change-profile-image/',
                    method: 'POST',
                    //thumbnailWidth: 150,
                    maxFilesize: 3,
                    paramName: "img",
                    maxFiles: 1,
                    acceptedFiles:'image/*',
                    createImageThumbnails: false,
                    //dictDefaultMessage: '<i class="material-icons left img-btn" style="margin: auto !important; left: 50%; top: 50%; position: absolute; transform: translateX(-50%) translateY(-50%); color:#0097a7 !important;" >camera_alt</i>',
                    previewTemplate: this.template(),
                    sending(file, xhr, formData) {
                        // Add the Authorization right before the request is sent
                        xhr.setRequestHeader('Authorization', 'Bearer ' + localStorage.getItem('access_token'));
                        Materialize.toast("Profile image changed", 3000, "rounded");
                    }
                },
                //thumbnail: '',
            };
        },
        components: {
            Transactions,
            vueDropzone: vue2Dropzone
        },
        computed: {
            first_name() {
                return this.$store.state.VisitedUser.first_name
            },
            last_name() {
                return this.$store.state.VisitedUser.last_name
            },
            full_name() {
                return this.first_name + ' ' +  this.last_name
            },
            username() {
                return this.$store.state.VisitedUser.username
            },
            profile_image() {
                return this.$store.state.VisitedUser.profile_image
            },
            bio() {
                return this.$store.state.VisitedUser.bio
            },
            isSelf() {
                return this.$store.state.User.username === this.$route.params.username
            },
            transactions() {
                return this.$store.state.UserTransactions
            }
        },
        methods: {
            logout: usersApi.logout,
            fetchUserInfo() {
                usersApi.userInfo(this.$route.params.username)
                if (this.isSelf) api.pendingTransactions()
            },
            editProfile(){
                this.modify = true;
            },
            saveProfile(){
                let email = this.$store.state.User.username;
                usersApi.editProfile(email, first_name.value, last_name.value, bio.value);
                this.$store.commit('updateProfileInfo',{
                    first_name: first_name.value,
                    last_name: last_name.value,
                    bio: bio.value
                });
                this.modify = false;
            },
            saveProfileImage(file, response){
                this.$store.commit('updateProfileImage',{
                    profile_image: response.res
                });
                console.log(this.$refs.binaryUploadZone);
                this.$refs.binaryUploadZone.removeAllFiles(true);
            },
            template: function () {
                console.log("template");
                return `<div class="dz-preview dz-file-preview circle">
                        <div class="dz-image circle">
                            <div data-dz-thumbnail-bg></div>
                        </div>
                        <div class="dz-details circle">
                            <div class="dz-size circle"><span data-dz-size></span></div>
                            <div class="dz-filename circle"><span data-dz-name></span></div>
                        </div>
                        <div class="dz-progress circle"><span class="dz-upload" data-dz-uploadprogress></span></div>
                        <div class="dz-error-message circle"><span data-dz-errormessage></span></div>
                        <div class="dz-success-mark circle"><i class="fa fa-check circle"></i></div>
                        <div class="dz-error-mark circle"><i class="fa fa-close circle"></i></div>
                    </div>
                `;
            },
        },
        watch: {
            '$route': function() {
                this.fetchUserInfo()
            }
        },
        created: function() {
            this.$store.commit('updateBreadcrumbs', {
                breadcrumbs: breadcrumbs
            })
    
            this.fetchUserInfo()
        },
    }
    $('#textarea').val('New Text');
    $('#textarea').trigger('autoresize');
</script>

<style lang="scss">

    .fixMargin {
        margin-top: 55px !important;
    }

    .light-green {
        color:#0097a7 !important;
    }

    .setting-button{
        margin-left: 70%;
    }

    #centerText {
        margin-left: 35px;
    }
    
    #cyan-darken2 {
        color: #0097a7;
    }
    
    .center-icon {
        margin-top: 12.5px;
    }
    
    .user-container {
        padding: 64px 32px;

        .row { margin: 0; }

        .card-panel {
            padding: 32px;
        }

        img {
            width: 100%;
            height: auto;
        }
        p {
            margin-top: 0;
            margin-bottom: 16px;
        }

        .user-info {
            .name-container,
            .email-container,
            .bio-container{
                h5 {
                    margin-top: 0;
                }  
                h6 {
                    font-size: 0.95rem;
                }
            }

            p:last-of-type { margin-bottom: 0; }
        }
    }

    div.profile-image:hover img{
        opacity:0.5;
    }
    div.profile-image:hover a {
        display: block;
    }
    div.profile-image a{
        position:absolute;
        display:none;
    }
    div.profile-image i.img-btn{
        top:0;
        left:0;
    }
    #customdropzone {
    position: absolute;
    top:20%;
    font-family: 'Arial', sans-serif;
    letter-spacing: 0.2px;
    color: #777;
    transition: background-color .2s linear;
    height: auto;
    padding: 40px;
  }

  #customdropzone .dz-preview {
    width: 160px;
    display: inline-block
  }
 #customdropzone .dz-preview .dz-image {
    width: 80px;
    height: 80px;
    margin-left: 40px;
    margin-bottom: 10px;
  }
  #customdropzone .dz-preview .dz-image > div {
    width: inherit;
    height: inherit;
    border-radius: 50%;
    background-size: contain;
  }
  #customdropzone .dz-preview .dz-image > img {
    width: 100%;
  }

   #customdropzone .dz-preview .dz-details {
    color: white;
    transition: opacity .2s linear;
    text-align: center;
  }
  #customdropzone .dz-success-mark, .dz-error-mark, .dz-remove {
    display: none;
  }
    
  
</style>