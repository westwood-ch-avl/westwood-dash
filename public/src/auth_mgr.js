//TODO -- how to handle when a user is signed out, or signed it, and I want logic to happen that is outside the realm of this auth UI? Need to find a way to *pass* this kind of event? Or pass a function *in* to this module? I could designate a class, for example ".for-signed-in-users", and then hide or delete such elements.

//I believe its possible to pass in a function to, say, the initialize_auth method, and then include that function in the callback. (This is because of something called "lexical scoping")

import { getAuth, signOut, onAuthStateChanged } from "firebase/auth";
import styles from "../auth_mgr.css" with { type: "css" };

export function set_up_auth(){

    document.adoptedStyleSheets.push(styles);

    buildHTML();

    initialize_auth();

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

    auth_menu.append(log_in_form);
    auth_menu.append(sign_out_form);
    auth_menu.append(sign_up_form);

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
}

function initialize_auth(){

    var jqi = $('#auth-menu-icon');

    const auth = getAuth();
    onAuthStateChanged(auth, (user) => {
        if (user) {
            // User is signed in, see docs for a list of available properties
            // https://firebase.google.com/docs/reference/js/auth.user
            const uid = user.uid;
            jqi.addClass('signed-in');
            
            user.getIdTokenResult(true)
                .then((idTokenResult) => {
                // Access your custom claim (for example, 'admin')
                if (idTokenResult.claims.admin) {

                    jqi.removeClass('signed-in');
                    jqi.addClass('signed-in-admin');
                    } 

                })
                .catch((error) => {
                console.error("Error fetching ID token result:", error);
                });

        } else {
            // User is signed out
            jqi.removeClass('signed-in');
            jqi.removeClass('signed-in-admin');
            // ...
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

        const auth = getAuth();
        signOut(auth).then(() => {

            close_auth_menu();

        }).catch((error) => {
            alert("Error: " + error.code + "\n" + error.message)
        });
    });

    $('#input-login-submit').on("click", function(){

        //handle clicking on the login button TODO
    });

    //TODO finish making the sign up form and handle clicks.

}
