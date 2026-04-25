const { default: makeWASocket, useMultiFileAuthState, delay } = require("@whiskeysockets/baileys");
const pino = require("pino");
const path = require("path");

async function getPairingCode(phoneNumber) {
    const sessionPath = path.join(__dirname, 'sessions', phoneNumber);
    const { state, saveCreds } = await useMultiFileAuthState(sessionPath);
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: false,
        logger: pino({ level: "silent" }),
        browser: ["Ubuntu", "Chrome", "20.0.04"]
    });
    if (!sock.authState.creds.registered) {
        await delay(5000);
        const code = await sock.requestPairingCode(phoneNumber);
        return code;
    }
    return "ALREADY_LINKED";
}

const args = process.argv.slice(2);
const num = args[0];
if (num) {
    getPairingCode(num).then(code => {
        process.stdout.write(code);
        process.exit(0);
    }).catch(err => {
        process.stderr.write(err.message);
        process.exit(1);
    });
}
