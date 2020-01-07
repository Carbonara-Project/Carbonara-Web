<template>
    <nav v-show="isAuthenticated">
        <div class="nav-wrapper row cyan darken-4">
            <div class="col s2 m1">
                <a href="#" data-activates="mobile-nav" class="button-collapse">
                    <i class="material-icons">menu</i>
                </a>
            </div>
            <div class="breadcrumb-container col s6 m6">
                <router-link v-for="b in breadcrumbs" 
                    class="breadcrumb" 
                    v-bind:key="b.path" 
                    v-bind:to="b.path"
                >
                    {{ b.label }}
                </router-link>
            </div>

            <ul class="side-nav" id="mobile-nav">
            </ul>

            <!-- Floating menu -->
            <div class="col s2 m1">
                <i id="floating-menu-trigger" class="material-icons dropdown-button" data-activates="floating-menu">person</i>
            </div>
            <ul id="floating-menu" class="dropdown-content">
                <li><router-link v-bind:to="profileLink">Profile</router-link></li>
                <li class="divider"></li>
                <li><a @click="logout" href="#!">Logout</a></li>
            </ul>

            <!-- Floating notifications -->
            <notification-list></notification-list>

        </div>
    </nav>
</template>
<script>
import usersApi from '../../api/users'
import NotificationList from './NotificationList'
import users from '../../api/users';

export default {
    name: 'navbar',
    components: {
        NotificationList
    },
    computed: {
        breadcrumbs() { return this.$store.state.breadcrumbs; },
        profileLink() { return '/user/' + this.$store.state.User.username; },
        isAuthenticated() { return this.$store.state.User.username !== "" }
    },
    methods: {
            logout: usersApi.logout
    },
    mounted: function() {

        $('.button-collapse').sideNav()
        $('#floating-menu-trigger').dropdown({
            inDuration: 300,
            outDuration: 225,
            constrainWidth: false, // Does not change width of dropdown to that of the activator
            hover: false, // Activate on hover
            gutter: 0, // Spacing from edge
            belowOrigin: true, // Displays dropdown below the button
            alignment: 'left', // Displays dropdown with edge aligned to the left of button
            stopPropagation: false // Stops event propagation
            }
        )
    }
}
</script>
<style lang="scss" scoped>
.breadcrumb-container a{
    &::first-of-type {
            @media only screen and (min-width: 993px) {
                padding-left: 18px;
        }
    }
}

#floating-menu-trigger{
    cursor: pointer;
}
</style>