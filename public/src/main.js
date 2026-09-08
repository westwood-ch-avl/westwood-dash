import { initializeApp } from 'firebase/app';
import { getAnalytics } from 'firebase/analytics';
import { getAuth, onAuthStateChanged, signInWithEmailAndPassword } from 'firebase/auth';
import { objs_to_csv_string } from './csv_tools.js';

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
const auth = getAuth(app);

$(function () {

    const auth = getAuth();
    onAuthStateChanged(auth, (user) => {
        if (user) {
            // User is signed in, see docs for a list of available properties
            // https://firebase.google.com/docs/reference/js/auth.user
            const uid = user.uid;
            $('#auth-menu-btn-img').addClass('signed-in');
            
            user.getIdTokenResult(true)
                .then((idTokenResult) => {
                // Access your custom claim (for example, 'admin')
                if (idTokenResult.claims.admin) {

                    $('#auth-menu-btn-img').removeClass('signed-in');
                    $('#auth-menu-btn-img').addClass('signed-in-admin');
                    } 

                })
                .catch((error) => {
                console.error("Error fetching ID token result:", error);
                });

        } else {
            // User is signed out
            $('#auth-menu-btn-img').removeClass('signed-in');
            $('#auth-menu-btn-img').removeClass('signed-in-admin');
            // ...
        }
    });

    $('#auth-menu-btn').on("click", function(){
        document.getElementById('log-in-dialog').showModal();
    });

    $('#input-login-submit').on("click", function(){
        email = $('#input-login-email').val();
        password = $('#input-login-password').val();
        document.getElementById('log-in-dialog').close();
        signInWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
                // Signed in 
            })
            .catch((error) => {
                const errorCode = error.code;
                const errorMessage = error.message;
                console.error("Error code: " + errorCode);
                console.error("Error Message: " + errorMessage)
            });
    });

});