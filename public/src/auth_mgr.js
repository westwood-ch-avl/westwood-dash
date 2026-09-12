//NOTES:
//1. this library assumes an option for "custom claims" where key is "admin" is true/false. You don't have to use it.
//2. this library does a lot of leg work for when a user change state happens. An additional optional function can be passed to be added to the handler.
//3. the "auth" object is attached to the window for use as a kind of global variable. It can referenced at `window.auth_mgr_auth` once everything is initialized.
//4. upon sign out, anything with class 'hwso' (hide when signed out will get the "d-none" class.) Anything with the class 'dwso' will be deleted from the DOM.
//5. upon sign-in, anything with the class 'swsi' (show when signed in) will get the class "d-none" removed if present. Similarly, 'swsia' will trigger for admin sign in.

import { getAuth, signOut, onAuthStateChanged, createUserWithEmailAndPassword } from "firebase/auth";
import styles from "../auth_mgr.css" with { type: "css" };

export function set_up_auth(optionalOnChangeFunc = undefined){

    document.adoptedStyleSheets.push(styles);

    buildHTML();

    initialize_auth(optionalOnChangeFunc);

    handle_handlers();

}

function buildHTML(){

    var auth_menu = $("<div style='display:fixed;top:1.5rem;right:2.5rem;' id='auth-menu'></div>");

    auth_menu_icon_holder = $("<div id='auth-menu-icon-holder' style='display:flex;flex-direction:row-reverse;filter:drop-shadow(0 0 0.75rem gray);border:1px solid gray;border-radius:1.5rem;background-color: white;padding:1px;'></div>");

    auth_menu.append(auth_menu_icon_holder);

    auth_menu_icon_holder.append("<img id='auth-menu-icon' style='width:3rem;height:3rem;' src='person-circle.svg'></img>");

    log_in_form = $("<div style='padding:1rem;' class='d-none' id='log_in_form'></div>");
    sign_out_form = $("<div class='d-none' id='sign_out_form' style='padding:1rem;'></div>");
    sign_up_form = $("<div class='d-none' id='sign_up_form' style='padding:1rem;'></div>");

    message_zone = $("<div style='padding:1rem;' class='d-none' id='auth-mgr-msg-zone'></div>");

    auth_menu.append(log_in_form);
    auth_menu.append(sign_out_form);
    auth_menu.append(sign_up_form);
    auth_menu.append(message_zone);

    $(body).append(auth_menu);

    log_in_form.append(`<p>Log In</p><form>
            <label for="input-login-email">email</label>
            <input id="input-login-email" type="email"/>
            <label for="input-login-password">password</label>
            <input id="input-login-password" type="password"/>
            <button class="btn btn-outline-secondary" type="submit" id="input-login-submit">Log In</button>
        </form>`);

    sign_out_form.append(`<div class="btn btn-outline-secondary" id='sign-out-btn'>Sign Out</div>`);

    sign_up_form.append(`<form><p>Sign Up</p></form>`); //TODO
}

function close_auth_menu(){

    $('#log_in_form').addClass('d-none');
    $('#sign_out_form').addClass('d-none');
    $('#sign_up_form').addCLass('d-none');
    $('#auth_mgr_msg_zone').addClass('d-none');
    $('#auth_mgr_msg_zone').html("");
}

function initialize_auth(){

    var jqi = $('#auth-menu-icon');

    const auth = getAuth();
    window.auth_mgr_auth = auth;

    onAuthStateChanged(auth, (user) => {
        if (user) {
            // User is signed in, see docs for a list of available properties
            // https://firebase.google.com/docs/reference/js/auth.user
            const uid = user.uid;
            jqi.addClass('signed-in');
            $('swsi').removeClass('d-none');
            
            user.getIdTokenResult(true)
                .then((idTokenResult) => {
                // Access your custom claim (for example, 'admin')
                if (idTokenResult.claims.admin) {

                    jqi.removeClass('signed-in');
                    jqi.addClass('signed-in-admin');
                    $('swsia').removeClass('d-none');
                    } 

                })
                .catch((error) => {
                console.error("Error fetching ID token result:", error);
                });

        } else {
            // User is signed out
            jqi.removeClass('signed-in');
            jqi.removeClass('signed-in-admin');
            $('.hwso').addClass('d-none');
            $('.dwso').remove();
        }

        if (optionalOnChangeFunc != undefined){
            optionalOnChangeFunc();
        }
    });

}

function handle_handlers(){

    $('#auth-menu-icon-holder').on("click", function(){

        if ( $('#log_in_form').hasClass('d-none') &&
        $('#sign_up_form').hasClass('d-none') &&
        $('#sign_out_form').hasClass('d-none')){

            jqi = $("#auth-menu-icon");

            if (jqi.hasClass('signed-in') || jqi.hasClass('signed-in-admin')){
                $('#sign_out_form').removeClass('d-none');
            }
            else{
                $('#log-in-form').removeClass('d-none');
            }

        }
        else{

            close_auth_menu();

        }

    });

    $('#sign-out-btn').on("click", function(){

        $('#sign-out-btn').prop('disabled', true);

        $('#auth-mgr-msg-zone').html("Waiting . . .");

        const auth = window.auth_mgr_auth;
        signOut(auth).then(() => {

            close_auth_menu();

        }).catch((error) => {

            $('#auth-mgr-msg-zone').html('<p>Error: ' + error.code + '</p><p>' + error.message + '</p>');
        }).finally(() => {

            $('#sign-out-btn').prop('disabled', false);
        });
    });

    $('#input-login-submit').on("click", function(){

        email = $('#input-login-email').val()
        password = $('#input-login-password').val()

        $('#input-login-submit').prop('disabled', true);

        $('#auth-mgr-msg-zone').html("Waiting . . .");

        const auth = window.auth_mgr_auth;
        signInWithEmailAndPassword(auth, email, password)
        .then((userCredential) => {
            // Signed in 
            const user = userCredential.user;

            close_auth_menu();
        })
        .catch((error) => {
            $('#auth-mgr-msg-zone').html('<p>Error: ' + error.code + '</p><p>' + error.message + '</p>');
            
        })
        .finally(() =>{
            $('#input-login-submit').prop('disabled', false);
        });

    });

    //TODO finish making the sign up form and handle clicks.

}
