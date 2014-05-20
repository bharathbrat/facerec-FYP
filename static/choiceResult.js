$(document).ready(function(){
/*setTimeout(function(){
console.log("yaaay");
window.location.href=window.location.href+"aa";
window.location.reload(true);
}, 0);*/
console.log("yaaay");
if(document.URL.indexOf("#")==-1)
 {
                // Set the URL to whatever it was plus "#".
                url = document.URL+"#";
                location = "#";
                setTimeout(function(){
                //Reload the page
                location.reload(true)},1);

            }
    
});
