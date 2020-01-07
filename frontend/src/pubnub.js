import store from './store'
import utils from './utils'

let pubnub = new PubNub({
    subscribeKey: "***",
    publishKey: "***",
    ssl: true
})

function vote_handler(msg) {
    msg.link = utils.createLinkForVote(msg)
    msg.content = utils.createContentForVote(msg)
    store.commit('loadNotification', msg)
    Materialize.toast(msg.content, 3000, 'rounded');
}

let handlers = {
    'vote': vote_handler
}

pubnub.addListener({
    message: function (m) {
        var actualChannel = m.actualChannel;
        var channelName = m.channel; // The channel for which the message belongs
        var msg = m.message; // The Payload
        var publisher = m.publisher;
        var subscribedChannel = m.subscribedChannel;
        var channelGroup = m.subscription; // The channel group or wildcard subscription match (if exists)
        var pubTT = m.timetoken; // Publish timetoken        
        console.log(
            actualChannel,
            channelName,
            msg,
            publisher,
            subscribedChannel,
            channelGroup,
            pubTT,
        )
        // Call handler for msg category
        handlers[msg.category](msg)
    },
    presence: function (p) {
        // handle presence
        var action = p.action; // Can be join, leave, state-change or timeout
        var channelName = p.channel; // The channel for which the message belongs
        var channelGroup = p.subscription; //  The channel group or wildcard subscription match (if exists)
        var presenceEventTime = p.timestamp; // Presence event timetoken
        var status = p.status; // 200
        var message = p.message; // OK
        var service = p.service; // service
        var uuids = p.uuids;  // UUIDs of users who are connected with the channel with their state
        var occupancy = p.occupancy; // No. of users connected with the channel
        // console.log(
        //     action,
        //     channelName,
        //     channelGroup,
        //     presenceEventTime,
        //     status,
        //     message,
        //     service,
        //     uuids,
        //     occupancy
        // )
    },
    status: function (s) {
        // handle status
        var category = s.category; // PNConnectedCategory
        var operation = s.operation; // PNSubscribeOperation
        var affectedChannels = s.affectedChannels; // The channels affected in the operation, of type array.
        var subscribedChannels = s.subscribedChannels; // All the current subscribed channels, of type array.
        var affectedChannelGroups = s.affectedChannelGroups; // The channel groups affected in the operation, of type array.
        var lastTimetoken = s.lastTimetoken; // The last timetoken used in the subscribe request, of type long.
        var currentTimetoken = s.currentTimetoken; // The current timetoken fetched in the subscribe response, which is going to be used in the next request, of type long.
        // console.log(
        //     category,
        //     operation,
        //     affectedChannels,
        //     subscribedChannels,
        //     affectedChannelGroups,
        //     lastTimetoken,
        //     currentTimetoken,
        // )
    }
});

// Publish prototype
// pubnub.publish(
//     {
//         message: {
//             such: 'object'
//         },
//         channel: 'ch1',
//         sendByPost: false, // true to send via post
//         storeInHistory: false, //override default storage options
//         meta: {
//             "cool": "meta"
//         } // publish extra meta with the request
//     },
//     function (status, response) {
//         // handle status, response
//     }
// );

function login(username) {
    pubnub.subscribe({
        channels: [username]
    })
}

function logout(username) {
    pubnub.unsubscribe({
        channels: [username]
    })
}

export default {
    login,
    logout
}
