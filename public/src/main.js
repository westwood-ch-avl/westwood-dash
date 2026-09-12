import { initializeApp } from 'firebase/app';
import { getAnalytics } from 'firebase/analytics';
import { objs_to_csv_string } from './csv_tools.js';
import { set_up_auth } from "auth_mgr.js";

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

    set_up_auth(); //This is a WIP...

});