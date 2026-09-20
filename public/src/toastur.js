export function buildToastContainer(){
    $(document.body).append(`<div class="toast-container bottom-0 end-0 p-4" style="margin-left:auto;margin-right:0px;"></div>`);
}

//set mintime to zero, and use a maxtime, for a regular Toast. Set maxtime to zero, and use a mintime, for a toast that will be removed by a callback. (Like a waiting notice.) NB: in the latter case, the below "done" function should be called inside of a "finally" step.
export function toasturStart(content, minTime=1000, maxTime = 0){

    let autohide = "";

    if(maxTime == 0 || maxTime == -1 || maxTime == undefined ){
        autohide = `data-bs-autohide="false"`;
    }
    else{
        autohide = `data-bs-delay="${maxTime.toString}"`;
    }

    let jqToastObject = $(`<div class="toast" ${autohide}}><div class="toast-body">${content}</div></div>`);

    let cont = $('.toast-container');

    cont.append(jqToastObject);

    let toastBootstrap = bootstrap.Toast.getOrCreateInstance(jqToastObject[0]);

    jqToastObject[0].dataset.start = Date.now();

    jqToastObject[0].dataset.minTime = minTime;

    toastBootstrap.show();

    jqToastObject[0].addEventListener('hidden.bs.toast', () => {
        toastBootstrap.dispose();
        jqToastObject.remove();
    });

    return jqToastObject;

}

export function toasturDone(jqToastObject){

    let elapsedTime = Date.now() - jqToastObject[0].dataset.start;
    
    let timeToWait = jqToastObject[0].dataset.minTime - elapsedTime;

    if (elapsedTime < 1)
    {
        bootstrap.Toast.getOrCreateInstance(jqToastObject[0]).hide();
    }
    else{
        setTimeout(function(){
            bootstrap.Toast.getOrCreateInstance(jqToastObject[0]).hide();
        }, timeToWait);
    }
}