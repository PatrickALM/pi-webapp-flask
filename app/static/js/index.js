
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

//rodar assim que a página index carregar
$(document).ready(function() {
    sleep(2000).then(() => { 
        console.log("oi")
       $('.alert-warning').fadeOut('slow');
    });  
});
