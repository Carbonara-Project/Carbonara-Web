<template>
    <div id="notifications-container">
        <div class="icon-container col s2 m4">
                <div v-show="notificationAlerts > 0" class="notification-alert">{{ notificationAlerts }}</div>
                <i 
                    id="floating-notifications-trigger" 
                    class="material-icons dropdown-button" 
                    data-activates="floating-notifications"
                    @click="clearNotificationAlerts"
                >notifications</i>
        </div>
        <ul id="floating-notifications" class="dropdown-content">
            <li v-for="n in notifications" :key="n.id">
                <router-link :to="n.link">
                    <div class="action">
                        <span class="new badge" data-badge-caption="">{{ n.category }}</span>
                        <time :datetime="n.creation_date">{{ notificationDate(n.creation_date) }}</time>
                    </div>
                    <div class="content">
                            <user-badge :email="n.by" :show-name="false"></user-badge>
                            <span>{{ n.content }}</span>
                    </div>
                </router-link>
            </li>
            <li v-if="notifications.length === 0">
                <span>You don't have any notification</span>
            </li>
        </ul>
    </div>
</template>
<script>
import moment from 'moment'
import UserBadge from '../User/UserBadge'

export default {
    name: 'notification-list',
    components: {
        UserBadge
    },
    computed: {
        notifications() {
            return this.$store.state.NotificationList
        },
        notificationAlerts() {
            return this.$store.state.NotificationAlerts
        }
    }, 
    methods: {
        notificationDate(date) {
            return moment(date).fromNow()
        },
        clearNotificationAlerts() {
            this.$store.commit('clearNotificationAlerts')
        }
    },
    mounted() {
        $('#floating-notifications-trigger').dropdown({
            inDuration: 300,
            outDuration: 225,
            constrainWidth: false, // Does not change width of dropdown to that of the activator
            hover: false, // Activate on hover
            gutter: 0, // Spacing from edge
            belowOrigin: true, // Displays dropdown below the button
            alignment: 'right', // Displays dropdown with edge aligned to the left of button
            stopPropagation: false // Stops event propagation
            }
        )
    }
}
</script>
<style lang="scss">
#notifications-container {
    .icon-container {
        position: relative;
        #floating-notifications-trigger {
            cursor: pointer;
        }
        .notification-alert {
            position: absolute;
            background-color: yellow;
            color: black;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            top: 10px;
            left: 20px;
        }
    }

    ul#floating-notifications{
        li {
            .action {
                display: flex;
                padding: 08px;

                .badge {
                    margin-left: 0;
                }

                time {
                    margin-left: 8px;
                }
            }
            .content {
                display: flex;
                align-items: flex-start;
                padding: 0px 8px;
                a {
                    padding: 0;
                    &:hover {
                        background-color: none;
                    }
                }
                span {
                    margin-left: 8px;
                }
            }
        }
    }
}
</style>
