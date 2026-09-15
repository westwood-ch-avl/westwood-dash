import { initializeApp } from 'firebase/app';
import { getAnalytics } from 'firebase/analytics';
import { objs_to_csv_string } from './csv_tools.js';
import { set_up_auth } from "./auth_mgr.js";
import { getFunctions, httpsCallable } from "firebase/functions";

const firebaseConfig = {
    apiKey: "AIzaSyBwyUE5DVV6SmZfK5jUXa5aTlacIf1StgE",
    authDomain: "wcha-ev-charging.firebaseapp.com",
    projectId: "wcha-ev-charging",
    storageBucket: "wcha-ev-charging.firebasestorage.app",
    messagingSenderId: "509620473785",
    appId: "1:509620473785:web:353bde88509f1592ce7068",
    measurementId: "G-1Y2WG7Q6XT"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

$(function () {

    $('#loading-msg').addClass('d-none');

    set_up_auth();

    $('#get-invite-code').on("click", function(){

        const functions = getFunctions(app, "us-east1");
        const get_fresh_invite_tokenv2 = httpsCallable(functions, 'get_fresh_invite_tokenv2');
        get_fresh_invite_tokenv2()
        .then((result) => {
            // Read result of the Cloud Function.
            /** @type {any} */
            const data = result.data;

            $('#invite-token-heading').removeClass("d-none");
            $('#invite-token-list').removeClass("d-none");
            $('#invite-token-list').append("<li>" + data["invite-token"] + "</li>");
        }).catch((error) => {
            alert("Error registered: " + error.code + "\n" + error.message + "\n" + error.details);
        });

    });

});