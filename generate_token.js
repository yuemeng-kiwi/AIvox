const { RtcTokenBuilder, RtcRole } = require('agora-access-token');

// Config from user
const appID = 'bd745b4aa7bd4c449f5f5291dfdc9a3f';
const appCertificate = 'bd745b4aa7bd4c449f5f5291dfdc9a3f'; // Using the same value as provided by user
const channelName = 'omotenashi-care';
const uid = 0; // 0 means any user can join with this token
const role = RtcRole.PUBLISHER;

const expirationTimeInSeconds = 3600 * 24; // 24 hours
const currentTimestamp = Math.floor(Date.now() / 1000);
const privilegeExpiredTs = currentTimestamp + expirationTimeInSeconds;

// Generate Token
const token = RtcTokenBuilder.buildTokenWithUid(appID, appCertificate, channelName, uid, role, privilegeExpiredTs);
console.log('Your Agora Token: ' + token);
